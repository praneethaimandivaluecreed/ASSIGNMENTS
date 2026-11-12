# Azure Data Factory – Metadata-Driven Pipelines
### Beginner Data Engineering Running Notes

## 1. What is a Metadata-Driven Pipeline?

Imagine a company has 100 tables that need to be loaded from a source database into a destination database.

One approach is to create 100 separate pipelines, one for each table.

But this creates problems:
- We have to create and maintain too many pipelines.
- If the loading logic changes, we may need to update many pipelines.
- Debugging and managing everything becomes difficult.
- Creating separate datasets for every table also increases maintenance work.

**Solution: Metadata-Driven Pipeline**

Instead of creating a separate pipeline for every table, we create one generic pipeline that reads instructions from a metadata/configuration table.

The metadata table tells ADF:
- Which source table to read.
- Where to load the data.
- Whether to perform a full or incremental load.
- Which column to use as a watermark, if required.
- Whether the table is enabled or disabled.

ADF reads these instructions and processes the tables dynamically.

**Simple analogy:** Think of a restaurant. The chef is the generic pipeline, and the order sheet is the metadata table. The chef follows the instructions for each order instead of learning a completely new process for every customer.

---

## 2. Metadata / Configuration Table

The first step is to create a configuration table that stores information about the tables we want to process.

### Important columns

| Column | Meaning |
|---|---|
| SourceSchema | Schema name of the source table (e.g., dbo). |
| SourceTable | Name of the source table (e.g., Customers). |
| TargetSchema | Schema name of the destination table. |
| TargetTable | Name of the destination table. |
| LoadType | Defines whether to perform FULL or INCREMENTAL loading. |
| WatermarkColumn | Column used to identify new or modified records (e.g., ModifiedDate). |
| IsEnabled | Indicates whether the table should be processed (1 = enabled, 0 = disabled). |

For CDC-based processing, we can also maintain:

| Column | Meaning |
|---|---|
| JoinKey | Key column(s) used to identify matching records in the source and target. |
| CheckpointKey | A unique identifier used to maintain CDC checkpoint state for a particular source/configuration. |

### Example configuration table

| SourceTable | TargetTable | LoadType | WatermarkColumn | IsEnabled |
|---|---|---|---|---|
| Customers | Customers | FULL | NULL | 1 |
| Products | Products | FULL | NULL | 1 |
| Orders | Orders | INCREMENTAL | ModifiedDate | 1 |
| Payments | Payments | INCREMENTAL | UpdatedAt | 1 |
| Employees | Employees | FULL | NULL | 0 |

Here:
- Customers and Products need full loads.
- Orders and Payments need incremental loads.
- Employees is disabled, so ADF should skip it.

**Important:** A configuration table stores instructions. It does not itself store the last successfully processed watermark. For a traditional watermark-based pipeline, we commonly maintain a separate watermark/control table to store that progress.

### How do we skip disabled tables?

We should process only records where `IsEnabled = 1`.

We can do this directly in the Lookup query:

```sql
SELECT *
FROM MetadataConfig
WHERE IsEnabled = 1;
```

Alternatively, we can retrieve the records and use a Filter activity before ForEach.

Filtering in the SQL query is usually simpler when the source supports it.

---

## 3. Lookup → ForEach → Parameterized Copy Pattern

This is the main design pattern used in a metadata-driven pipeline.

### Overall flow

```text
Lookup_Config
      |
      v
   ForEach
      |
      v
  Copy Activity
      |
      v
 Destination
```

### Step 1: Lookup Activity

Lookup reads the enabled records from the metadata table.

For processing multiple table configurations, configure:

- First row only = False

The output contains an array called `value`.

Example output:

```json
{
  "count": "2",
  "value": [
    {
      "SourceTable": "Customers",
      "TargetTable": "Customers"
    },
    {
      "SourceTable": "Orders",
      "TargetTable": "Orders"
    }
  ]
}
```

### Step 2: ForEach Activity

ForEach processes each record returned by Lookup.

Items expression:

```text
@activity('Lookup_Config').output.value
```

**Important:** ForEach requires an array (a list of items), not a single object.

- First row only = False returns multiple records in `value`.
- First row only = True returns one record under `firstRow`.

Therefore, for our multi-table pattern, use First row only = False and pass the `value` array.

Inside ForEach, `@item()` represents the current configuration record.

Examples:

```text
@item().SourceTable
@item().TargetTable
@item().LoadType
@item().SourceSchema
@item().TargetSchema
```

If the current record is Orders, `@item().SourceTable` returns Orders.

### Step 3: Parameterized Datasets

Instead of creating separate datasets for every table, create reusable datasets with parameters.

For example, create a source dataset called `DS_SQL_Source`.

Dataset parameter:

```text
TableName (String)
```

In the dataset's table name property, use:

```text
@dataset().TableName
```

Now, in the Copy activity, pass:

```text
TableName = @item().SourceTable
```

For the target dataset, do the same:

```text
TableName = @item().TargetTable
```

We can also parameterize schema names and file names when required.

### How does the value travel?

```text
Metadata Table
      |
      v
Lookup returns table records
      |
      v
ForEach gets current record
      |
      v
@item().SourceTable
      |
      v
Copy Activity passes dataset parameter
      |
      v
@dataset().TableName
      |
      v
ADF reads the correct table
```

**Remember the difference:**

- `@item()` refers to the current ForEach record.
- `@pipeline().parameters.Name` refers to a pipeline parameter.
- `@dataset().Name` refers to a dataset parameter.

The parameter names and values must be mapped correctly. Always check the runtime Input of the activity when debugging a parameter mismatch.

---

## 4. One Generic Pipeline for Many Tables – Full vs Incremental Load

The main advantage of a metadata-driven pipeline is that the same pipeline can process different tables using different loading strategies.

We can use an If Condition or Switch activity inside ForEach to check the LoadType.

```text
ForEach
   |
   v
Check LoadType
   |
   |---- FULL
   |       |
   |       v
   |   Full Copy
   |
   |---- INCREMENTAL
           |
           v
      Read old watermark
           |
           v
      Find new watermark
           |
           v
      Copy changed records
           |
           v
      Update watermark
```

### 4.1 Full Load

Full load means copying all the required records from the source table to the destination.

Example:

```sql
SELECT * FROM Customers;
```

Every run reads the complete source data.

**Important:** Full load does not automatically mean the target is truncated or replaced. The destination write behavior depends on the Copy activity and sink configuration.

If we append all records on every run, duplicates may occur. We must choose the correct target loading strategy.

### 4.2 Incremental Load using a Watermark

Incremental load means copying only new or modified records instead of copying the complete table every time.

A watermark is a value that tells us how far we have processed the source data.

Example watermark column:

```text
ModifiedDate
```

We commonly maintain a separate watermark table:

| TableName | LastWatermark |
|---|---|
| Orders | 2026-11-11 23:59:00 |
| Payments | 2026-11-11 22:30:00 |

Suppose the last successful watermark for Orders is:

```text
2026-11-11 23:59:00
```

Now we find the latest available ModifiedDate in the source. Suppose it is:

```text
2026-11-12 14:00:00
```

We copy records in this range:

```sql
SELECT *
FROM Orders
WHERE ModifiedDate > @OldWatermark
  AND ModifiedDate <= @NewWatermark;
```

After the data is loaded successfully, we update the stored watermark to the new value.

**Why do we update the watermark only after a successful load?**

If the Copy activity fails and we update the watermark anyway, some records may never be loaded during the next run.

Therefore, update the watermark only after successful processing.

### 4.3 Avoid duplicates during reruns

Suppose a pipeline fails after loading some records.

If we simply rerun the pipeline and append all those records again, duplicates may occur.

A safer database loading strategy is:

1. Copy delta records into a staging table.
2. Use a primary/business key to identify matching records.
3. Insert new records.
4. Update existing records.
5. Complete the merge successfully.
6. Update the watermark.

This is commonly implemented using SQL MERGE or an upsert strategy.

This makes the process more reliable when rerunning after failures.

### Important limitations of watermark-based loading

- A timestamp watermark can identify inserts and updates only when the column is updated correctly.
- It cannot automatically detect deleted records.
- If a source update does not change the watermark column, that update may be missed.
- Late-arriving records and records with identical timestamps need careful handling.
- A safe target strategy is necessary to prevent duplicates.

For deletes and more complete change tracking, database CDC or Change Tracking may be more suitable.

---

## 5. CDC and Checkpoints in Mapping Data Flows

CDC means **Change Data Capture**.

It helps identify changes made in the source database, such as:

- Insert – a new record is added.
- Update – an existing record is modified.
- Delete – a record is deleted.

### 5.1 Watermark vs CDC

These are two different ways of identifying changes.

**Watermark-based approach:**

ADF checks a column such as ModifiedDate and asks:

"Give me the records whose ModifiedDate is greater than my last saved watermark."

This depends on a reliable incremental column.

**Native database CDC approach:**

The database tracks changes using its own change-tracking mechanism. ADF can read these changes without requiring us to identify changes through a timestamp column.

For SQL Server CDC:

1. CDC must be enabled on the database and the required source table.
2. SQL Server creates internal CDC change tables, such as `cdc.dbo_Orders_CT` (the exact name depends on the capture instance).
3. Database changes are captured from the transaction log by the CDC capture process.
4. The change records contain information about the operation and its ordering.
5. ADF reads the changes and can identify inserts, updates, and deletes.

**LSN (Log Sequence Number):**

An LSN is a sequential identifier associated with database log records. It helps track the order and position of changes in the transaction log.

Think of it as a receipt/reference number that helps the database identify where a change occurred.

### 5.2 CDC in ADF Mapping Data Flow

ADF Mapping Data Flow supports native CDC for supported sources, including SQL Server and Azure SQL Database.

A basic design:

```text
Parameterized Source Dataset
          |
          v
     Data Flow
          |
          v
  Source with Native CDC
          |
          v
   Transformations
          |
          v
       Sink
```

The source uses native CDC settings to detect changes.

The sink can apply the required operations:

- Allow insert
- Allow update
- Allow delete
- Allow upsert

For database sinks, the appropriate key column(s) must be configured to identify the matching destination records.

**Important distinction:** With native CDC sources, ADF already understands the incoming change-operation markers, so an Alter Row transformation is not required just to identify native CDC insert/update/delete operations. For other sources, Alter Row may be needed to define the operations.

### 5.3 What is a checkpoint?

A checkpoint represents the progress of CDC processing.

It helps ADF know where to continue reading changes from during the next execution.

Think of it like a bookmark in a book:

- First run: ADF starts reading changes from the configured starting point.
- After processing: ADF maintains checkpoint state.
- Next run: ADF continues from the previously processed position.

**Checkpoint vs watermark:**

| Watermark | CDC checkpoint |
|---|---|
| Usually based on a source column such as ModifiedDate | Maintains CDC processing progress |
| We commonly manage the watermark value in a control table | ADF manages CDC checkpoint state |
| Identifies rows using a comparison on a column | Tracks the change position using the CDC mechanism |
| Does not automatically identify deletes | Can capture deletes when supported by the source CDC implementation |

They serve a similar purpose of remembering progress, but they are not the same mechanism.

### 5.4 Checkpoint key in ADF

When we use CDC in a Mapping Data Flow, the Data Flow activity has a checkpoint key setting.

- ADF maintains checkpoint state for CDC processing.
- A checkpoint key can be overridden.
- The checkpoint key helps identify the CDC processing state.
- If the same data flow is reused for multiple source tables through a ForEach, we should consider using a separate checkpoint key for each source/configuration.

For example:

```text
@item().CheckpointKey
```

This allows the current metadata record to supply its checkpoint key.

ADF's current Data Flow activity documentation describes a GUID-based default checkpoint key, which helps preserve CDC state even if activity names change. You can override it when you need to manage checkpoint identity explicitly.

**Important:** Do not confuse the checkpoint key with the watermark column. The checkpoint key identifies CDC state; it is not itself the ModifiedDate value.

### 5.5 Metadata-driven CDC pipeline design

Suppose we have multiple source tables and want to reuse one Data Flow.

We can create:

1. Parameterized source dataset.
2. Parameterized sink dataset.
3. Mapping Data Flow using the source and sink datasets.
4. Lookup activity to read metadata.
5. ForEach activity to process each metadata record.
6. Data Flow activity inside ForEach, passing the current record's parameters.

Example metadata:

| Column | Example |
|---|---|
| SourceSchema | dbo |
| SourceTable | Orders |
| TargetSchema | dbo |
| TargetTable | Orders |
| JoinKey | OrderID |
| CheckpointKey | Orders_CDC |
| IsEnabled | 1 |

We pass the required values into the Data Flow parameters:

```text
SourceSchema = @item().SourceSchema
SourceTable = @item().SourceTable

TargetSchema = @item().TargetSchema
TargetTable = @item().TargetTable

JoinKey = @item().JoinKey

CheckpointKey = @item().CheckpointKey
```

Inside the Data Flow, these parameters are used by the source and sink configurations.

The source reads changes from the correct table. The sink writes to the correct target table using the appropriate key.

**Why is this useful?**

Without metadata-driven processing, we might need to create separate datasets and Data Flow configurations for many tables. With parameterization, we can reuse common logic and manage table-specific settings through metadata.

**Important considerations:**

- The source and target schemas must be compatible with the generic Data Flow design.
- Join keys must exist in the target mapping and correctly identify records.
- The checkpoint key should be unique for each independent CDC stream/configuration.
- Do not share one checkpoint between unrelated source tables.
- CDC support and options depend on the source connector.
- Do not force incompatible sources into one generic design. Use specialized pipelines or Data Flows when their requirements differ.

---

## 6. Batch Count, Timeouts and Throttling

### 6.1 Batch Count

Batch count controls how many ForEach iterations can execute at the same time when parallel execution is enabled.

Example:

We have 10 tables and set:

```text
isSequential = False
batchCount = 3
```

ADF can process up to 3 iterations simultaneously. When an iteration finishes, another can start.

Important facts:

- Maximum parallel iterations = 50.
- Default batchCount = 20.
- Batch count is an upper concurrency limit, not a guarantee that all iterations will always run at that number.
- If sequential execution is enabled, batch count does not control parallel execution.

Use a lower batch count if the source database or destination is getting overloaded.

### 6.2 Timeout

Timeout is the maximum time an activity is allowed to run before ADF marks it as timed out.

Example:

If an activity has a timeout of 30 minutes and it is still running after 30 minutes, it may fail with a timeout error.

Possible causes:
- Slow database queries.
- Large amounts of data.
- Network problems.
- Overloaded Integration Runtime.
- Slow destination system.

Do not immediately increase the timeout. First investigate why the activity is taking longer than expected.

### 6.3 Throttling

Throttling happens when a service receives more requests than it can handle or when a service limit is reached.

Example:

Suppose 20 Copy activities run simultaneously against a database that can comfortably handle only 5.

The database may become overloaded, slow down, or reject requests.

For APIs, a common response is:

```text
HTTP 429 - Too Many Requests
```

How to handle throttling:

- Reduce ForEach batch count.
- Reduce unnecessary concurrent requests.
- Check source and destination capacity.
- Configure appropriate retries and retry intervals.
- Follow service-provided retry guidance where available.

### Quick difference

| Concept | Meaning |
|---|---|
| Batch count | How many iterations can run at once |
| Timeout | How long an activity is allowed to run |
| Throttling | Service limiting requests because of capacity or rate limits |

---

## 7. Debugging Metadata-Driven Pipelines

### 7.1 Find which table failed inside ForEach

Suppose the pipeline processes four tables:

| Table | Status |
|---|---|
| Customers | Succeeded |
| Products | Succeeded |
| Orders | Failed |
| Payments | Succeeded |

How do we find the problem?

1. Open Monitor in ADF Studio.
2. Find the failed pipeline run.
3. Open the ForEach activity's iteration details.
4. Identify the failed iteration.
5. Check which table was being processed.
6. Open the failed inner activity, such as Copy or Data Flow.
7. Inspect its Input, Output, and error message.
8. Fix the issue and rerun safely.

We can also add User Properties to important activities:

```text
SourceTable = @item().SourceTable
TargetTable = @item().TargetTable
LoadType = @item().LoadType
```

This makes table-level information easier to see in Monitor.

### 7.2 Parameter mismatch

Example:

The metadata record contains:

```text
SourceTable = Orders
```

But the Copy activity reads Customers.

Possible causes:

- Wrong `@item()` property.
- Dataset parameter name mismatch.
- Copy activity did not pass the dataset parameter.
- Dataset uses a hardcoded table name.
- Wrong parameter type or value.

Debugging steps:

1. Inspect Lookup output.
2. Check the current ForEach item.
3. Open the Copy activity Input.
4. Verify the actual parameter values.
5. Check dataset parameter definitions.
6. Correct the mapping.

### 7.3 Empty Lookup

A Lookup can succeed but return zero rows.

Example:

```json
{
  "count": "0",
  "value": []
}
```

ForEach receives an empty array and executes zero iterations.

Possible causes:

- Configuration table is empty.
- All tables are disabled.
- Wrong WHERE condition.
- Wrong database or schema.
- Incorrect query.
- Missing metadata record.

We can check the number of returned rows using:

```text
@greater(
    length(activity('Lookup_Config').output.value),
    0
)
```

If records exist, continue to ForEach.

If no records exist, either:
- Fail the pipeline with a meaningful error if tables must always be processed.
- Log a message and finish successfully if an empty result is expected.

**Important Lookup limits:**
- Maximum 5,000 rows.
- Maximum output size of 4 MB.

### 7.4 Other important debugging points

- A successful pipeline does not always mean data was processed. Lookup may have returned zero rows.
- Do not increase retry count for permanent errors such as an incorrect table name.
- Do not increase batch count to fix a parameter mismatch.
- Parallel ForEach iterations share pipeline variables. Avoid using Set Variable to store the current table name inside parallel iterations because values can overwrite each other.
- If a Copy fails after partially writing data, check whether rerunning can create duplicates.
- Use staging and MERGE/upsert strategies to make reruns safer.
- Check the actual runtime Input and Output instead of assuming expressions worked correctly.

---

## 8. Readable Naming and Folders

A pipeline should be easy for another data engineer to understand and maintain.

Avoid names like:

```text
Pipeline1
Copy1
Lookup1
Dataset1
```

Use meaningful names instead:

| Object | Example name |
|---|---|
| Pipeline | PL_MetadataDriven_LoadTables |
| Lookup | LKP_EnabledTableConfig |
| ForEach | FE_ProcessTables |
| Copy | CP_CopySourceToTarget |
| If Condition | IF_IsFullLoad |
| Dataset | DS_SQL_Source |
| Linked Service | LS_AzureSQL_Source |
| Data Flow | DF_CDC_TableSync |

These prefixes are naming conventions, not mandatory ADF keywords.

### Example folder organization

```text
Pipelines/
│
├── 01_Ingestion/
│   ├── PL_MetadataDriven_LoadTables
│   └── PL_LoadReferenceData
│
├── 02_Transformation/
│   └── PL_TransformSales
│
└── 03_Orchestration/
    └── PL_Master_DailyETL


Datasets/
├── DS_SQL_Source
├── DS_SQL_Target
└── DS_ADLS_Raw


LinkedServices/
├── LS_AzureSQL_Source
└── LS_ADLS_Target
```

### Other good practices

- Use meaningful activity names.
- Add descriptions to important activities.
- Use folders to group related pipelines.
- Use User Properties to expose important runtime values.
- Keep metadata and watermark tables organized.
- Avoid unnecessary duplicate pipelines and datasets.
- Use common logic wherever possible, but do not force incompatible sources into one generic design.

**Goal:** Another engineer should be able to open the pipeline and understand what it does without needing to ask the person who created it.

---

## 9. Quick Revision – Important Interview Points

| Interview question | Key answer |
|---|---|
| Why use metadata-driven pipelines? | To reuse one generic pipeline for multiple tables and reduce maintenance. |
| Why do we need a metadata table? | It stores source, target, load type, watermark, and enabled information. |
| Why First row only = False? | We need an array of multiple records for ForEach. |
| What does `@item()` mean? | It represents the current ForEach record. |
| What is a parameterized dataset? | A reusable dataset whose table, schema, or file path can change dynamically. |
| Full vs incremental load? | Full copies all required records; incremental copies only new or changed records. |
| Why use a watermark table? | To remember the last successfully processed value for each table. |
| Why use staging and MERGE? | To avoid duplicates and safely insert or update records during reruns. |
| What is CDC? | A method of capturing inserts, updates, and deletes from supported source databases. |
| What is a checkpoint? | It tracks CDC processing progress so the next run can continue from the saved position. |
| What is batch count? | The maximum number of concurrent ForEach iterations allowed. |
| What is throttling? | A service limiting requests because its capacity or rate limit is reached. |
| How do you find a failed table? | Monitor → pipeline run → ForEach iteration details → failed inner activity. |
| Why can Lookup return empty? | Wrong query/filter, disabled tables, missing metadata, or wrong database. |
| Why use meaningful names and folders? | To make pipelines easier to understand, debug, and maintain. |

### Final concept to remember

A metadata-driven pipeline separates **instructions from execution**.

The metadata table tells ADF what to process. Lookup retrieves those instructions. ForEach processes each configuration record. Parameterized datasets and Data Flows dynamically select the correct source and target. The load logic decides whether to perform a full load, watermark-based incremental load, or CDC-based change processing.

This makes the solution reusable, scalable, and easier to maintain—provided that we handle checkpoints, failures, parameter mappings, and destination writes correctly.