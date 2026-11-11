# AZURE DATA FACTORY – MAPPING DATA FLOWS
## Beginner-Friendly Running Notes

---

# PAGE 1 – INTRODUCTION TO MAPPING DATA FLOWS

## 1. What is a Mapping Data Flow?

Mapping Data Flow is a feature in Azure Data Factory (ADF) that helps us **clean, transform and process data without writing Spark code manually**.

We can perform operations such as:
- Removing unwanted rows.
- Creating new columns.
- Joining two tables.
- Grouping data.
- Removing duplicates.
- Changing the structure of data.

We do all these operations using a visual interface.

**Simple example:**

Suppose we have a customer file containing:

| customer_id | name | age |
|---|---|---:|
| C01 | Ravi | 22 |
| C02 | Priya | 25 |
| C03 | Anu | 17 |

We want to:
1. Remove customers below 18.
2. Create a new column called `status`.
3. Save the final data into a database.

We can do all this using Mapping Data Flow.

## 2. How Does Mapping Data Flow Work?

Mapping Data Flow uses **Apache Spark behind the scenes**.

We design the transformations visually, and ADF manages the Spark execution.

We don't have to manually write Spark code or manage every Spark operation.

Remember this:

- We design the logic in ADF.
- Spark performs the actual processing.
- ADF manages the execution environment.

## 3. Two Types of Data Flows in ADF

ADF provides two types:

| Type | Purpose |
|---|---|
| Mapping Data Flow | Visual data transformation using Spark |
| Wrangling Data Flow | Data preparation using a Power Query-based experience |

In this syllabus, we are mainly learning Mapping Data Flow.

## 4. Understanding the Data Flow Canvas

When we open a Mapping Data Flow, we mainly work with three areas:

**1. Top bar**

Contains options for saving, debugging and managing the Data Flow.

**2. Graph / Canvas**

This is where we build the data processing flow by connecting transformations.

**3. Configuration panel**

When we select a transformation, its settings appear here.

For example, if we select a Filter transformation, we configure the filter condition in this panel.

## 5. The Three Main Parts of a Data Flow

Every basic Mapping Data Flow has three important parts:

### Source – Where data comes from

Examples:
- CSV file.
- Parquet file.
- SQL Server table.
- Azure Data Lake file.

### Transformation – What we do with the data

Examples:
- Filter unwanted records.
- Join two tables.
- Create new columns.
- Calculate total sales.

### Sink – Where the final data goes

Examples:
- Azure SQL Database.
- Azure Data Lake Storage.
- Parquet files.
- Azure Synapse Analytics.

**Remember this simple flow:**

`Source → Transformation → Sink`

Example:

`Customers.csv → Remove invalid records → Azure SQL Database`

## 6. Dataset vs Inline Dataset

When configuring a Source or Sink, we can use a normal Dataset or an Inline Dataset.

### Dataset

A Dataset is a separate, reusable object in ADF.

We create it once and can use it in multiple pipelines or Data Flows.

Example: A reusable dataset representing a customer CSV file.

### Inline Dataset

An Inline Dataset is defined directly inside the Source or Sink transformation.

We don't need to create a separate Dataset object.

Think of it this way:

- Dataset = Saving an address in your address book so you can reuse it.
- Inline Dataset = Writing the address directly on one delivery package.

| Feature | Dataset | Inline Dataset |
|---|---|---|
| Where defined? | Separate ADF object | Inside the transformation |
| Reusability | Can be reused | Specific to that Data Flow |
| Best for | Common, repeated sources | Dynamic or one-time sources |

Inline datasets are useful when working with dynamic file paths, flexible schemas and different file configurations.

**Important:** Neither a Dataset nor an Inline Dataset changes the original source file. They describe how ADF connects to and reads the data.

---

# PAGE 2 – SOURCE, SCHEMA AND COMMON TRANSFORMATIONS

## 1. Understanding the Source

The Source is the starting point of our Data Flow.

It tells ADF:
- Where the data is stored.
- Which file or table to read.
- What format the data uses.
- What columns and data types are available.

### Source file formats

Examples:
- CSV
- JSON
- Parquet
- Avro
- SQL tables

### Why do CSV files have delimiter settings?

A CSV file stores data as text.

Example:

`C01,Ravi,22`

ADF needs to understand how the values are separated.

That is why CSV settings include:

| Setting | Meaning |
|---|---|
| Column delimiter | Separates columns, such as comma |
| Row delimiter | Separates records, such as newline |
| Encoding | Defines how characters are represented |
| Escape character | Allows special characters to be treated as normal text |
| Quote character | Identifies text enclosed in quotation marks |

For example:

`C01,"Ravi, Kumar",22`

The comma inside `"Ravi, Kumar"` should not be treated as a column separator.

The quote character helps ADF understand this.

**What about Parquet and Avro?**

Parquet and Avro are structured file formats. They store schema information with the data.

Therefore, ADF can read their structural information without requiring us to configure CSV-style delimiters.

## 2. What is Projection?

Projection is the list of columns and their data types that ADF understands for a source.

Example:

| Column | Data type |
|---|---|
| customer_id | String |
| age | Integer |
| salary | Decimal |

Think of Projection as the **blueprint of the incoming data**.

It tells ADF what columns it should expect.

### Import Schema

When we click Import Schema, ADF reads the source and identifies its columns and data types.

For Mapping Data Flow, this operation uses the available debug compute environment.

That is why Debug mode needs to be enabled when importing or previewing source metadata through the Data Flow experience.

## 3. Source Schema Options

There are four important options.

### Allow Schema Drift

Allows new or unexpected columns to pass through the Data Flow.

Example:

Today the source has:

`id, name, age`

Tomorrow it has:

`id, name, age, city`

Allow Schema Drift helps ADF handle the additional `city` column.

### Infer Drifted Column Types

When new columns appear, ADF can try to identify their data types.

If type inference is disabled, drifted columns are generally treated as strings.

### Validate Schema

Checks whether the incoming data matches the expected schema.

If the source structure does not match the expected projection, validation can fail.

### Use Projected Schema

Uses the schema already defined in the Data Flow instead of discovering the schema from every incoming file.

This can be useful when processing many files with a known structure.

**Easy way to remember:**

| Option | What it does |
|---|---|
| Allow Schema Drift | Accept new columns |
| Infer Drifted Column Types | Identify types of new columns |
| Validate Schema | Check expected structure |
| Use Projected Schema | Use the defined schema |

## 4. Common Transformations

### A. Select Transformation

Select is used to choose which columns should continue in the Data Flow.

Example:

Input:

`customer_id, name, age, salary, address`

We only need:

`customer_id, name, age`

Using Select, we can remove `salary` and `address`.

We can also rename or reorder columns.

### B. Derived Column Transformation

Derived Column is used to create new columns or modify existing columns.

Example:

| quantity | price |
|---:|---:|
| 2 | 500 |
| 3 | 200 |

We want to calculate total amount.

Expression:

`quantity * price`

New column:

`total_amount`

Result:

| quantity | price | total_amount |
|---:|---:|---:|
| 2 | 500 | 1000 |
| 3 | 200 | 600 |

### C. Filter Transformation

Filter removes records that do not satisfy a condition.

Example:

We only want customers whose age is at least 18.

Condition:

`age >= 18`

Records below 18 are removed from the output stream.

### D. Join Transformation

Join combines two data streams using a matching column.

Customers:

| customer_id | name |
|---|---|
| C01 | Ravi |
| C02 | Priya |

Orders:

| customer_id | amount |
|---|---:|
| C01 | 500 |
| C02 | 1000 |

Join condition:

`Customers.customer_id = Orders.customer_id`

Result:

| customer_id | name | amount |
|---|---|---:|
| C01 | Ravi | 500 |
| C02 | Priya | 1000 |

### E. Aggregate Transformation

Aggregate is used to group records and calculate summary values.

Example:

| customer | amount |
|---|---:|
| Ravi | 500 |
| Ravi | 300 |
| Priya | 700 |

Group by: `customer`

Aggregate: `sum(amount)`

Result:

| customer | total_amount |
|---|---:|
| Ravi | 800 |
| Priya | 700 |

Common aggregate functions:
- SUM
- COUNT
- AVG
- MIN
- MAX

### F. Sort Transformation

Sort arranges records in a particular order.

Example:

Sort customers by age in descending order.

`age DESC`

The highest age appears first.

**Remember the difference:**

- Filter removes rows.
- Select removes or changes columns.
- Derived Column creates or modifies columns.
- Aggregate groups rows and calculates values.
- Sort changes the order of rows.

---

# PAGE 3 – DEBUG MODE, DATA PREVIEW AND EXPRESSION BUILDER

## 1. What is Debug Mode?

Debug mode helps us test a Mapping Data Flow before running the complete pipeline.

When we turn on Debug mode, ADF starts or connects to a temporary Spark environment called the **Debug Cluster**.

Think of it as a practice laboratory.

We can test our transformations and see how the data changes at every step.

### Why do we need Debug mode?

Suppose we created a Derived Column transformation.

We want to check whether our expression is calculating the correct result.

Instead of running the complete pipeline every time, we can use Data Preview to check the output.

## 2. How to Enable Debug Mode

1. Open the Mapping Data Flow.
2. Find the Debug option.
3. Turn Debug mode ON.
4. Wait for the debug cluster to become ready.
5. Open Data Preview.
6. Select the transformation you want to inspect.

When we finish testing, turn Debug mode OFF to release the debug compute resources.

### Important: What happens to the Sink in Debug mode?

Data Preview is used to inspect data. It does not write the previewed records to the final Sink.

However, running a pipeline in Debug mode can execute the Data Flow activity and write to its Sink.

So, do not assume every Debug operation is completely write-free. Be careful when the destination is a production database or storage location.

## 3. Debug Settings

We can configure how much data is used during testing.

For example:
- Row limit.
- Parameters.
- Sampling settings, where available.

**Why use sample data?**

Suppose the actual source contains 10 lakh records.

For testing a simple expression, we may only need a small sample.

Using a smaller sample makes testing easier and faster.

But remember: A small sample may not reveal problems that occur only with large datasets, such as skew or memory issues.

## 4. Data Preview

Data Preview shows us the data at a selected transformation.

Example:

`Source → Filter → Derived Column → Sink`

We can select:
- Source to see original data.
- Filter to see which rows remain.
- Derived Column to see the new column.
- Other transformations to inspect their output.

This helps us identify exactly where something went wrong.

### Quick Actions in Data Preview

When we select a column header, ADF provides useful actions.

Examples:
- Change data type.
- Rename a column.
- Remove a column.
- Modify a column.

ADF can automatically create the required transformation logic when we use these actions.

For example, changing a column's type can create a Derived Column operation.

### Data Profiling

Data Profiling gives us basic statistics about a column.

For a text column, we can inspect things such as:
- NULL values.
- Empty values.
- Distinct values.

For a numeric column, we can inspect:
- Minimum.
- Maximum.
- Average.
- Distribution statistics.

Think of it like using `describe()` in Pandas to understand a column.

**Remember:** Data Preview and profiling are useful for understanding data, but they may use only a sample. They are not always a replacement for checking the complete production dataset.

## 5. What is the Expression Builder?

Expression Builder is where we write the logic used in Data Flow transformations.

It provides functions for:
- Calculations.
- String operations.
- Date operations.
- NULL handling.
- Conditional logic.
- Type conversion.

### Important expressions

| Expression | Purpose |
|---|---|
| `iif()` | Checks a condition |
| `isNull()` | Checks whether a value is NULL |
| `coalesce()` | Returns the first non-NULL value |
| `concat()` | Joins strings |
| `trim()` | Removes spaces at the beginning and end |
| `toInteger()` | Converts a value into an integer |
| `toDate()` | Converts a value into a date |
| `lower()` | Converts text to lowercase |
| `upper()` | Converts text to uppercase |
| `guid()` | Generates a GUID |

Examples:

**Create a full name:**

`concat(first_name, ' ', last_name)`

**Replace a NULL city:**

`iif(isNull(city), 'Unknown', city)`

**Calculate total amount:**

`quantity * unit_price`

**Convert text to lowercase:**

`lower(email)`

**Important:** Mapping Data Flow expressions and pipeline expressions are different expression environments. Do not blindly copy an expression from one into the other.

---

# PAGE 4 – SCHEMA DRIFT, NULL HANDLING AND DATA TYPE ERRORS

## 1. What is Schema Drift?

Schema Drift means the structure of incoming data changes over time.

Example:

Monday:

| id | name | age |
|---|---|---:|
| 1 | Ravi | 22 |

Friday:

| id | name | age | city |
|---|---|---:|---|
| 1 | Ravi | 22 | Hyderabad |

A new column called `city` has appeared.

If the source schema is fixed, ADF may not automatically recognize that new column.

By enabling Schema Drift, we can allow new columns to pass through the Data Flow.

### How do we access drifted columns?

We can use:
- `byName()` – access a column by its name.
- `byPosition()` – access a column by its position.
- Column patterns – apply logic to multiple columns matching a condition.
- Map Drifted – create mappings for drifted columns.

Example:

`byName('city')`

This helps us access a column that was not present in the original projection.

**Important:** Schema Drift provides flexibility, but we must still check important business columns. Otherwise, unexpected changes may silently enter the output.

## 2. Understanding NULL Values

NULL means a value is missing or unknown.

It is not the same as zero or an empty string.

| Value | Meaning |
|---|---|
| NULL | Missing value |
| 0 | Numeric zero |
| `''` | Empty string |
| `'   '` | Spaces |
| `'null'` | Actual text |
| false | Boolean false |

### How to check NULL?

`isNull(city)`

### How to keep non-NULL values?

`!isNull(city)`

### How to replace NULL?

`coalesce(city, 'Unknown')`

### How to handle NULL and empty strings?

`iif(isNull(city) || trim(city) == '', 'Unknown', trim(city))`

**Important:** Do not replace every NULL with zero.

For example, if salary is NULL, it does not necessarily mean the employee earns zero. The value may simply be missing.

Always follow the business rule.

## 3. What if a Mandatory Column is NULL?

Example:

| customer_id | name |
|---|---|
| C01 | Ravi |
| NULL | Priya |
| C03 | Anu |

Suppose customer ID is mandatory.

We should not create a random customer ID for Priya.

Instead:
- Valid records go to the main output.
- Invalid records go to a reject or quarantine location.
- We investigate whether the missing value can be corrected.

We can use Filter or Conditional Split for this.

## 4. Column Name Mismatch

Suppose the actual source column is:

`customer_name`

But our expression uses:

`customerName`

ADF may show a ColumnNotFound error.

Possible reasons:
- Wrong spelling.
- Column was renamed.
- Projection is outdated.
- Source schema changed.
- Expression refers to a column that is not available at that transformation.

### How to fix it?

1. Open the Source.
2. Check the Projection tab.
3. Verify the actual column names.
4. Refresh/import the schema if necessary.
5. Check the expressions in later transformations.
6. Use Select to rename columns when required.

## 5. Data Type Errors

Every column has a data type.

Examples:

| Column | Expected type |
|---|---|
| age | Integer |
| salary | Decimal |
| joining_date | Date |
| is_active | Boolean |
| name | String |

Suppose age contains:

`20, 25, Twenty, 30`

If we convert `Twenty` into an integer, conversion fails.

### Safer way to handle it

1. Keep the original value.
2. Remove unnecessary spaces.
3. Validate whether the value can be converted.
4. Convert valid records.
5. Send invalid records to a reject stream.

Example functions:

`isInteger(trim(age_text))`

`toInteger(trim(age_text))`

`toDate(joining_date, 'dd-MM-yyyy')`

Also check:
- Decimal precision and scale.
- Date format.
- Boolean values.
- Source and Sink data types.

## 6. Validate Schema

There are two places where schema validation matters.

**Source Validate Schema:** Checks whether incoming source data matches the expected schema.

**Sink Validate Schema:** Checks whether the output is compatible with the destination schema.

Remember: Even if we never change the original source file, a Data Flow can fail because the incoming structure does not match what ADF expects.

---

# PAGE 5 – CHOOSING BETWEEN COPY ACTIVITY, DATA FLOW AND SPARK NOTEBOOK

These three tools are used for different purposes.

## 1. Copy Activity – Mainly for Moving Data

Think of Copy Activity as a delivery truck.

It takes data from one location and moves it to another.

Examples:
- SQL Server → ADLS.
- CSV → Parquet.
- Blob Storage → Azure SQL Database.

Copy Activity also supports:
- Column mapping.
- Supported data type conversion.
- File format conversion.
- Compression and decompression.
- Parallel copy.
- Staging.
- Supported fault-tolerance options.

Use Copy Activity when your main requirement is moving data.

## 2. Mapping Data Flow – For Visual Transformations

Mapping Data Flow is useful when we want to transform data visually without writing Spark code.

Examples:
- Join two tables.
- Remove invalid records.
- Create new columns.
- Calculate total sales.
- Group data by customer.
- Split valid and invalid records.

It runs on Spark-based compute managed by ADF.

Use it when the required transformations can be handled clearly using its visual interface.

## 3. Spark Notebook – For Custom Code

A Spark Notebook is useful when we need more control over the processing logic.

Examples:
- Complex PySpark operations.
- Advanced JSON processing.
- Custom algorithms.
- Machine learning preparation.
- Reusable processing frameworks.

ADF can execute a Databricks Notebook using the Databricks Notebook activity.

**Important:** The notebook runs on Databricks compute, not on the ADF Mapping Data Flow debug cluster.

## 4. Quick Comparison

| Feature | Copy Activity | Mapping Data Flow | Spark Notebook |
|---|---|---|---|
| Main purpose | Move data | Visual transformation | Custom processing |
| Coding | Usually minimal | No Spark code needed | PySpark/Scala |
| Compute | Copy infrastructure | Managed Spark | Databricks/Synapse Spark |
| Best for | Data ingestion | Joins, filters, aggregates | Complex logic |

## 5. How to Choose?

Ask yourself:

**Only need to move data?**

Choose Copy Activity.

**Need visual transformations?**

Choose Mapping Data Flow.

**Need complex custom Spark logic?**

Choose Spark Notebook.

Also remember: If data is already inside a database and SQL can perform the required transformation efficiently, a SQL query or stored procedure may be the better choice.

## 6. Can We Combine Them?

Yes!

Example:

`Copy Activity → Mapping Data Flow → Databricks Notebook`

1. Copy raw customer data into ADLS.
2. Use Mapping Data Flow to clean and join the data.
3. Use a Databricks Notebook for advanced processing.

**Interview point:** Choose a tool based on the requirement, complexity, performance, cost and maintainability.

---

# PAGE 6 – ADVANCED TRANSFORMATIONS: WINDOW, PIVOT, UNPIVOT, SURROGATE KEY, EXISTS AND LOOKUP

## 1. Window Transformation

Window transformation is used to calculate values over a group of related rows.

Unlike Aggregate, it does not necessarily reduce the number of rows.

Example:

| customer | date | amount |
|---|---|---:|
| Ravi | Jan 1 | 500 |
| Ravi | Jan 2 | 700 |
| Ravi | Jan 3 | 300 |

We want to calculate Ravi's running total.

| customer | amount | running_total |
|---|---:|---:|
| Ravi | 500 | 500 |
| Ravi | 700 | 1200 |
| Ravi | 300 | 1500 |

Window configuration has four important areas:

| Setting | Meaning |
|---|---|
| Over | Defines the group or partition |
| Sort | Defines the order of rows |
| Range by | Defines which rows are included in the window |
| Window columns | Defines the calculations |

Common window functions:
- `rowNumber()`
- `rank()`
- `denseRank()`
- `sum()`
- `avg()`
- `lag()`
- `lead()`
- `cumeDist()`

### What is CUME_DIST?

CUME_DIST means Cumulative Distribution.

It tells us the proportion of rows whose values are less than or equal to the current row's value within the window partition.

Example:

If 8 out of 10 rows have values less than or equal to the current row:

`CUME_DIST = 8 / 10 = 0.8`

Its result ranges from 0 to 1.

## 2. Pivot Transformation

Pivot converts rows into columns.

Example input:

| department | month | sales |
|---|---|---:|
| IT | Jan | 100 |
| IT | Feb | 200 |
| HR | Jan | 150 |
| HR | Feb | 250 |

After Pivot:

| department | Jan | Feb |
|---|---:|---:|
| IT | 100 | 200 |
| HR | 150 | 250 |

Important settings:
- Group by – identifies each output row.
- Pivot key – contains the values that become column names.
- Pivot columns – contains the values or expressions to calculate.

## 3. Unpivot Transformation

Unpivot does the opposite of Pivot.

It converts columns into rows.

Input:

| department | Jan | Feb |
|---|---:|---:|
| IT | 100 | 200 |
| HR | 150 | 250 |

Output:

| department | month | sales |
|---|---|---:|
| IT | Jan | 100 |
| IT | Feb | 200 |
| HR | Jan | 150 |
| HR | Feb | 250 |

Important settings:
- Ungroup by – columns that remain unchanged.
- Unpivot key – stores the original column names.
- Unpivot columns – columns that are converted into rows.

**Easy memory trick:**
- Pivot: Rows → Columns.
- Unpivot: Columns → Rows.

## 4. Surrogate Key Transformation

A Surrogate Key is an artificial ID created for records.

Example:

| customer_name | customer_key |
|---|---:|
| Ravi | 1 |
| Priya | 2 |
| Anu | 3 |

It is commonly used in data warehouse dimension tables.

Why do we need it?

- Business IDs may change.
- A source may not have a suitable unique ID.
- We need a stable identifier for dimension records.

**Do not confuse these:**

| Term | Meaning |
|---|---|
| Surrogate key | Artificial key, often sequential |
| GUID | Globally unique identifier |
| Pipeline Run ID | Identifies one pipeline execution |

They serve different purposes.

## 5. Exists Transformation

Exists checks whether a record from one stream has a matching record in another stream.

Example:

Customers:

`C01, C02, C03`

Active customers:

`C01, C03`

Using Exists, we keep:

`C01, C03`

Using Doesn't Exist, we keep:

`C02`

It is useful when we only need to check whether a match exists.

## 6. Lookup Transformation

Lookup finds matching information from another stream.

Example:

Orders:

| product_id | quantity |
|---|---:|
| P01 | 2 |
| P02 | 3 |

Products:

| product_id | product_name |
|---|---|
| P01 | Laptop |
| P02 | Mouse |

Using Lookup, we can attach product names to orders.

The `isMatch()` function can help us identify whether a Lookup found a matching record.

## 7. Difference Between Join, Exists and Lookup

| Transformation | Purpose |
|---|---|
| Join | Combines columns from two streams |
| Exists | Checks whether a matching record exists |
| Lookup | Finds matching reference information |

---

# PAGE 7 – CONDITIONAL SPLIT, MULTIPLE SINKS AND DEDUPLICATION

## 1. Conditional Split

Conditional Split divides one data stream into multiple streams based on conditions.

Example:

| order_id | amount |
|---|---:|
| O01 | 500 |
| O02 | 5000 |
| O03 | 10000 |
| O04 | 200 |

We want three categories:

- High value: amount > 5000.
- Medium value: amount between 1000 and 5000.
- Low value: amount < 1000.

We can create three output streams using Conditional Split.

### Two important options

**First matching condition**

A record goes to the first output whose condition is satisfied.

**All matching conditions**

A record can go into more than one output if multiple conditions match.

Example:

If one record satisfies both Condition A and Condition B:

- First matching condition: It goes only to the first matching output.
- All matching conditions: It can go to both outputs.

## 2. Multiple Sinks

A Data Flow can have more than one Sink.

Example:

After processing customer data, we want:

- Valid customers → Customer database.
- Invalid customers → Reject file.
- Summary data → Reporting table.

We can create separate branches and connect them to different Sinks.

### Important Sink execution settings

By default:
- Sinks are executed sequentially.
- They belong to the same group initially.
- A sink error can fail the Data Flow.

We can configure different sink groups and priorities to control execution behaviour.

## 3. Deduplication

Deduplication means removing unwanted duplicate records.

Example:

| customer_id | name | updated_at |
|---|---|---|
| C01 | Ravi | Jan 1 |
| C01 | Ravi Kumar | Jan 5 |
| C02 | Priya | Jan 3 |

Suppose we want only the latest record for each customer.

**Can we simply use Distinct?**

No. Distinct removes duplicate rows based on selected columns. It does not automatically mean that the latest record will be retained.

### Correct approach

1. Group records by `customer_id` using a window partition.
2. Sort by `updated_at` in descending order.
3. Generate a row number.
4. Keep only the row where row number is 1.

Concept:

`Partition by customer_id`

`Sort by updated_at DESC`

`Keep row_number = 1`

Now we get the latest customer record.

**Important:** First decide what makes a record a duplicate. It may be the customer ID, email, or a combination of columns.

## 4. Deduplication vs Aggregation

| Deduplication | Aggregation |
|---|---|
| Removes unwanted duplicates | Combines records into summaries |
| Can keep one selected record | Calculates SUM, COUNT, AVG, etc. |
| Example: Keep latest customer record | Example: Total sales per customer |

---

# PAGE 8 – SLOWLY CHANGING DIMENSIONS AND FLOWLETS

## 1. What is a Slowly Changing Dimension?

In a Data Warehouse, dimension tables store descriptive information about business entities.

Examples:
- Customers.
- Products.
- Employees.
- Locations.

Suppose Ravi is living in Hyderabad.

Later, he moves to Bengaluru.

The question is:

**Should we replace Hyderabad with Bengaluru, or should we keep both values as history?**

This is where Slowly Changing Dimensions (SCD) are used.

## 2. SCD Type 1 – Overwrite Old Data

SCD Type 1 replaces the old value with the new value.

Before:

| customer_id | name | city |
|---|---|---|
| C01 | Ravi | Hyderabad |

After:

| customer_id | name | city |
|---|---|---|
| C01 | Ravi | Bengaluru |

The old city is lost.

Use Type 1 when we do not need to maintain history.

Example: Correcting a spelling mistake.

## 3. SCD Type 2 – Maintain History

SCD Type 2 keeps the old record and inserts a new version.

Before:

| customer_key | customer_id | city | is_current |
|---:|---|---|---|
| 101 | C01 | Hyderabad | true |

After:

| customer_key | customer_id | city | is_current |
|---:|---|---|---|
| 101 | C01 | Hyderabad | false |
| 102 | C01 | Bengaluru | true |

Now we can see both the old and new cities.

Common SCD Type 2 columns:

- Surrogate key.
- Business key.
- Start date.
- End date.
- Current-record flag.

## 4. How to Implement SCD in Mapping Data Flow

A typical process looks like this:

**Step 1: Read new customer records.**

Read the incoming data.

**Step 2: Read existing dimension records.**

Read the current customer dimension table.

**Step 3: Join both streams.**

Use the business key, such as `customer_id`.

**Step 4: Compare the columns.**

Check whether the customer's city, name or other tracked attributes have changed.

**Step 5: Separate the records.**

We identify:
- New customers.
- Changed customers.
- Unchanged customers.

**Step 6: Apply the correct action.**

- New customer → Insert.
- Unchanged customer → Ignore.
- Changed customer → Update for Type 1.
- Changed customer → Expire old version and insert a new version for Type 2.

**Step 7: Write the results to the dimension table.**

Use the appropriate Sink settings and write operations.

## 5. What is Alter Row?

Alter Row is used to define what should happen to each record at a supported Sink.

It can mark records for:
- Insert.
- Update.
- Delete.
- Upsert.

Example:

If a customer's city changes and we are implementing Type 1, we can mark that record for Update.

**Important:** Alter Row does not automatically implement the complete SCD logic. We must build the matching, comparison, expiration and insertion logic ourselves.

## 6. What is a Flowlet?

A Flowlet is a reusable group of Data Flow transformations.

Imagine three Data Flows need the same customer-cleaning logic:

- Remove extra spaces.
- Convert email to lowercase.
- Standardize phone numbers.
- Validate customer IDs.

Instead of creating the same logic three times, we can create one Flowlet and reuse it.

Think of a Flowlet as a reusable function for Data Flow transformations.

### Advantages

- Reuse existing logic.
- Avoid repeating transformations.
- Maintain the same business rules.
- Make Data Flows easier to manage.

---

# PAGE 9 – DATA FLOW MONITORING

## 1. Why Do We Need Monitoring?

Creating a Data Flow is not enough.

After execution, we need to know:

- Did it succeed?
- How many records were read?
- How many records were written?
- Which transformation took the most time?
- Did the Join increase the number of records?
- Are some partitions processing more data than others?

ADF provides a Data Flow monitoring view to investigate these questions.

## 2. Four Main Performance Areas

A Data Flow can be slow for four major reasons.

### 1. Cluster Startup Time

How long does Spark take to start?

A new Spark cluster may take several minutes to become ready.

### 2. Source Reading Time

How long does it take to read the input data?

Possible reasons for slowness:
- Very large files.
- Slow source systems.
- Network problems.
- Poor source configuration.

### 3. Transformation Processing Time

How long does Spark take to process the data?

Possible reasons:
- Expensive Join.
- Large Aggregate.
- Data skew.
- Unnecessary transformations.

### 4. Sink Writing Time

How long does it take to write the final output?

Possible reasons:
- Slow destination.
- Large output.
- Too many small files.
- Destination write limitations.

**Remember:** A slow Data Flow is not always a compute problem. First find which stage is slow.

## 3. How to Open the Monitoring View

1. Run the pipeline.
2. Open ADF Monitor.
3. Find the pipeline run.
4. Open the Data Flow activity details.
5. Open the monitoring/graph view.

Here we can inspect:
- Stage timings.
- Row counts.
- Transformation execution.
- Partition statistics.
- Column lineage.

## 4. Stage Timings

Stage timings show how much time each stage takes.

Example:

| Stage | Time |
|---|---:|
| Source | 20 seconds |
| Join | 180 seconds |
| Aggregate | 30 seconds |
| Sink | 40 seconds |

The Join takes the most time.

So, we should investigate the Join first.

We should not immediately increase the cluster.

## 5. Row Counts

Row counts show how many records pass through each transformation.

Example:

| Transformation | Rows |
|---|---:|
| Source | 100,000 |
| Filter | 80,000 |
| Join | 120,000 |
| Aggregate | 5,000 |
| Sink | 5,000 |

What can we understand?

- Filter removed 20,000 rows.
- Join increased the count to 120,000.
- Aggregate reduced the records to 5,000.

The Join output increased. We should check whether this is expected or caused by duplicate keys.

## 6. Partition Statistics

Spark divides data into partitions so that multiple tasks can process it in parallel.

Ideally, data should be distributed reasonably evenly.

Example:

| Partition | Records |
|---|---:|
| P1 | 10,000 |
| P2 | 12,000 |
| P3 | 11,000 |
| P4 | 500,000 |

P4 has much more data than the other partitions.

This may indicate data skew.

ADF monitoring can provide partition statistics, including skewness and kurtosis, to help us understand the data distribution.

## 7. Column Lineage

Column lineage tells us where output columns came from.

| Type | Meaning |
|---|---|
| Mapped | Came from a source column and is mapped to the Sink |
| Derived | Created during a transformation |
| Computed | Used for processing or expressions, but not necessarily written to the Sink |

Example:

- `customer_id` → Mapped.
- `total_amount` → Derived.
- `is_valid` used only in a Filter → Computed.

## 8. My Monitoring Approach

If a Data Flow normally takes 2 minutes but suddenly takes 12 minutes:

1. Check cluster startup time.
2. Check source reading time.
3. Find the slowest transformation.
4. Check row counts before and after Join.
5. Inspect partition statistics.
6. Check sink writing time.
7. Fix the actual bottleneck.
8. Run again and compare the results.

**Remember:** Monitoring is not just checking success or failure. It helps us understand how the Data Flow performed.

---

# PAGE 10 – RUNTIME SETTINGS, CLUSTER STARTUP AND DEBUGGING

## 1. Data Flow Activity Settings

When we add a Data Flow activity to a pipeline, we can configure its execution settings.

Important settings include:

| Setting | Purpose |
|---|---|
| Integration Runtime | Defines the execution environment |
| Compute type | Defines the type of compute |
| Core count | Controls the configured compute size |
| TTL | Keeps eligible compute available for reuse |
| Checkpoint key | Identifies CDC checkpoint state |
| Staging / PolyBase | Supports bulk loading into Synapse |
| Logging level | Controls execution details collected |
| First Row Only | Limits Cache sink output passed to the pipeline |

## 2. Compute Types

ADF provides compute options such as:

| Compute type | Simple meaning |
|---|---|
| General purpose | Balanced compute and memory |
| Compute optimized | More processing power |
| Memory optimized | More memory for memory-heavy workloads |

Choose the compute type according to the workload.

Do not select a larger cluster without first understanding the performance problem.

## 3. Cold Start and Warm Cluster

### Cold Start

A new Spark cluster must be created and started.

This can take several minutes.

### Warm Cluster

An existing eligible cluster can be reused instead of creating a new one.

This can reduce startup time.

## 4. What is TTL?

TTL means Time to Live.

It controls how long an eligible Spark cluster remains available after a job finishes.

Example: TTL = 10 minutes.

- Data Flow A finishes at 10:00 AM.
- The cluster remains available.
- Data Flow B starts at 10:05 AM.
- If the same eligible compute environment can be reused, startup overhead can be reduced.
- After the idle TTL expires, the cluster is released.

**Important:** AutoResolve does not automatically mean warm start, and a custom Integration Runtime does not automatically mean cold start. Cluster reuse depends on availability and configuration.

Debug compute and triggered pipeline execution also have separate configuration settings.

## 5. Debug Cluster vs Pipeline Execution

| Debug mode | Pipeline execution |
|---|---|
| Used for development and testing | Used for actual pipeline execution |
| Uses debug compute configuration | Uses Data Flow activity execution configuration |
| Useful for Data Preview | Processes the actual pipeline workload |
| Often tested with sample data | May process the complete dataset |

A Data Flow working in Debug mode does not guarantee that production execution will succeed.

The production environment may have:
- More data.
- Different permissions.
- Different runtime settings.
- Different source or sink conditions.

## 6. PolyBase Staging

Suppose we need to load millions of records into Azure Synapse Analytics.

Loading records individually can be slow.

PolyBase supports bulk loading through a temporary staging location in Azure Blob Storage or ADLS.

Think of it like this:

- Row-by-row loading = carrying one item at a time.
- Bulk loading = transporting a complete shipment together.

It is useful for large Synapse loading workloads when the source, sink and staging configuration support it.

## 7. Logging Levels

Logging levels control how much execution information ADF collects.

| Level | Meaning |
|---|---|
| Verbose / Fine | Detailed partition-level information |
| Basic / Coarse | Transformation execution durations |
| None | High-level summary |

Use detailed logging when investigating a problem.

For normal production runs, use a lower level if detailed information is not required.

## 8. CDC Checkpoint Key

CDC means Change Data Capture.

It helps us process only new or changed records instead of processing everything repeatedly.

Think of a checkpoint as a bookmark.

Example:

- First run processes changes up to a particular point.
- The checkpoint remembers the progress.
- The next run continues from the saved position.

ADF manages checkpoints for supported CDC scenarios.

The default checkpoint key is based on a hash of the Data Flow name and pipeline name.

If different source streams or tables need separate checkpoint states, the checkpoint key must be designed carefully.

## 9. GUID vs Run ID vs Surrogate Key

These three are different.

| Term | Meaning |
|---|---|
| GUID | Globally Unique Identifier |
| Pipeline Run ID | Identifies one pipeline execution |
| Surrogate key | Artificial key for a business record |

ADF pipeline expressions include `guid()` to generate a GUID.

A GUID can be used as an identifier when required, but it is not the same as a sequential surrogate key.

## 10. Cache Sink and First Row Only

A Cache sink can pass a small result from a Data Flow into a later pipeline activity.

The pipeline output has a 2 MB limit.

**First Row Only unchecked:**

ADF attempts to return all rows from the Cache sink within the output limit.

If the output exceeds the limit, the activity can fail.

**First Row Only checked:**

ADF returns only the first row from the Cache sink.

It does not mean the Data Flow processed only one row. It only limits the result passed back to the pipeline.

Use this when you need a small result, such as a summary value, rather than an entire dataset.

## 11. Debug Cluster Not Starting

Possible reasons:

- Compute provisioning issue.
- Wrong or unavailable Integration Runtime.
- Network or firewall problem.
- Private endpoint or DNS issue.
- Unhealthy debug session.

### How to troubleshoot?

1. Read the exact error.
2. Check the debug compute configuration.
3. Wait if the cluster is still provisioning.
4. Check the Integration Runtime and region.
5. Check network and storage connectivity.
6. Restart an unhealthy debug session if needed.
7. Try again with a small sample.

**Important:** If the cluster is already running but Source Preview fails, check the linked service, credentials, permissions, file path and schema. Do not keep restarting the cluster unnecessarily.

## 12. Quick Debugging Table

| Problem | First thing to check |
|---|---|
| Cluster not starting | Debug compute and IR |
| Preview fails | Source connection and permissions |
| Column not found | Projection and expression |
| NULL values | NULL handling and business rules |
| Conversion error | Actual input format and data type |
| Sink fails | Sink mapping and destination schema |
| New column appears | Schema drift and projection |
| Debug works but production fails | Runtime, permissions, data size and settings |

---

# PAGE 11 – PERFORMANCE TROUBLESHOOTING AND INTERVIEW QUESTIONS

## 1. Join Explosion

Join explosion happens when the Join output becomes much larger than expected.

Example:

Left table:

| customer_id |
|---|
| C01 |
| C01 |
| C02 |

Right table:

| customer_id | order_id |
|---|---|
| C01 | O01 |
| C01 | O02 |
| C02 | O03 |

For C01:

- Left side has 2 matching records.
- Right side has 2 matching records.
- Join output has 2 × 2 = 4 combinations.

This happens because duplicate keys exist on both sides.

### What should I check?

1. Check the Join condition.
2. Check duplicate keys on both sides.
3. Understand whether the relationship should be one-to-one or one-to-many.
4. Check whether the increased output is expected.
5. Fix duplicate data if necessary.

**Important:** Do not immediately increase the Spark cluster. More compute cannot fix incorrect Join logic.

## 2. Data Skew

Spark divides data into partitions so that multiple tasks can process it.

Ideally, each partition should receive a reasonable amount of data.

But sometimes one partition receives much more data than the others.

Example:

| Partition | Records |
|---|---:|
| P1 | 10,000 |
| P2 | 12,000 |
| P3 | 11,000 |
| P4 | 500,000 |

P4 takes much longer to process.

This is called Data Skew.

### Why does it happen?

- Some keys appear very frequently.
- Many records have NULL or default Join keys.
- A few customers have unusually high activity.
- Join or Aggregate operations group too many records under one key.

### How to fix it?

1. Check partition statistics.
2. Identify frequently occurring keys.
3. Remove unnecessary records early.
4. Broadcast a genuinely small dataset when appropriate.
5. Consider repartitioning.
6. Isolate hot keys or use advanced techniques such as salting when necessary.

**Remember:** Increasing the number of partitions does not always solve skew. If the same hot key continues to go into one partition, that partition can remain overloaded.

## 3. Out of Memory (OOM)

OOM means Out of Memory.

It happens when Spark does not have enough memory to complete an operation.

Common reasons:

- Very large partitions.
- Data skew.
- Join explosion.
- Large Sort or Aggregate.
- Broadcasting a large dataset.
- Too many concurrent workloads.

### How to troubleshoot?

1. Find which transformation failed.
2. Check whether Join output increased unexpectedly.
3. Check partition sizes.
4. Check whether a large stream is being broadcast.
5. Remove unnecessary columns and rows early.
6. Adjust partitioning if required.
7. Increase compute or use memory-optimized compute if the workload genuinely needs it.

**Important:** Do not increase memory before checking whether the data is unnecessarily large.

## 4. Timeout

Timeout means an operation did not finish within the allowed time.

Different operations can time out.

| Timeout | Possible reason |
|---|---|
| Cluster startup | Compute provisioning problem |
| Source | Slow source or connection |
| Broadcast | Broadcast operation takes too long |
| Sink | Destination is slow |
| Activity | Overall activity exceeded its timeout |

For broadcast joins, Microsoft documents default timeouts of 60 seconds for Debug runs and 300 seconds for job runs.

If the broadcast stream is too large:
- Turn broadcast OFF.
- Broadcast the smaller stream instead.
- Use Auto when appropriate.
- Increase compute when justified.

Do not blindly increase timeout values. First understand why the operation is taking so long.

## 5. What Should I Change First?

| Problem | First action |
|---|---|
| Join output increased | Check Join condition and duplicate keys |
| One partition is slow | Check data skew and hot keys |
| OOM | Check partition size, Join and broadcast |
| Broadcast timeout | Check broadcast stream size |
| Source is slow | Check source reading and connectivity |
| Sink is slow | Check destination and write performance |
| Cluster starts slowly | Check startup time, IR and TTL |

### My debugging order

1. Read the exact error message.
2. Open the monitoring view.
3. Identify the failed or slow stage.
4. Check row counts.
5. Check Join conditions and duplicates.
6. Check partition statistics.
7. Check memory, broadcast and source/sink settings.
8. Increase compute or timeout only if necessary.
9. Run again and compare the result.

---

## 6. Scenario-Based Interview Questions

### Q1. Your Data Flow takes 10 minutes just to start. What will you do?

**Answer:** I will check the cluster startup time. If the Data Flow runs frequently, I will check whether TTL and cluster reuse can reduce the startup overhead.

### Q2. Your Join output increases from 50,000 to 5 lakh records. What will you check?

**Answer:** I will check the Join condition and duplicate keys on both sides. I will verify whether the relationship is one-to-one or one-to-many before changing the compute.

### Q3. Your Data Flow works with small files but fails with large files. Why?

**Answer:** Large data may cause memory issues, skew or longer processing time. I will check partition statistics and the slow transformations first.

### Q4. One Spark partition is taking much longer than the others. What could be the reason?

**Answer:** It may be data skew. I will check whether some keys contain too many records.

### Q5. A new column is added to your source every week. How will you handle it?

**Answer:** I can enable Schema Drift and use flexible column references. I will still validate important business columns.

### Q6. Your Data Flow shows ColumnNotFound. What will you do?

**Answer:** I will check the source projection and verify the column names used in later transformations. I will refresh the projection if the source schema has changed.

### Q7. Your age column contains 20, 25 and Twenty. How will you handle it?

**Answer:** I will validate the values before converting them. Valid records will be converted into integers, and invalid records will go to a reject stream.

### Q8. Your customer ID column contains NULL values. Will you replace them with zero?

**Answer:** No. A missing customer ID is not the same as zero. I will follow the business rule and send invalid records to a quarantine stream if the ID is mandatory.

### Q9. Your Data Flow works in Debug mode but fails in production. Why?

**Answer:** Debug mode may use sample data and different compute settings. I will compare runtime settings, permissions, parameters, source data size and Sink configuration.

### Q10. You need to convert CSV into Parquet without complex transformations. What will you use?

**Answer:** Copy Activity, because the main requirement is moving data and converting its format.

### Q11. You need to join three tables, filter invalid rows and calculate total sales. What will you use?

**Answer:** Mapping Data Flow, because it provides visual transformations such as Join, Filter and Aggregate.

### Q12. You need complicated custom PySpark logic. What will you use?

**Answer:** A Spark Notebook, such as a Databricks Notebook, because it gives more control over custom Spark processing.

### Q13. Your Data Flow takes 15 minutes, and the Join takes 12 minutes. What will you do?

**Answer:** I will investigate the Join condition, duplicate keys, input sizes and partition distribution. I will optimize the Join before increasing compute.

### Q14. Your pipeline writes to Synapse very slowly. What can you try?

**Answer:** I will check the sink writing time and see whether PolyBase staging can be used for bulk loading.

### Q15. Your Cache sink output fails because it is too large. What will you do?

**Answer:** I will avoid passing the complete dataset through pipeline activity output because it has a 2 MB limit. I will store the data in a proper destination instead. If I only need one result, I can use First Row Only.

### Q16. You need to send valid and invalid customer records to different destinations. What will you use?

**Answer:** I will use Conditional Split to separate the records and connect each output to a different Sink.

### Q17. A customer changes their city, and the business wants to retain the previous city. Which SCD type will you use?

**Answer:** SCD Type 2, because it preserves historical records by creating a new version.

### Q18. Three Data Flows need the same customer-cleaning logic. What will you use?

**Answer:** A Flowlet, because it allows us to reuse the same transformation logic.

### Q19. Source Preview fails, but the debug cluster is already running. What will you check?

**Answer:** I will check the linked service, credentials, permissions, firewall, source path and projection. I will not restart the cluster without checking these things.

### Q20. Should we add Sort before every Join to improve performance?

**Answer:** No. Mapping Data Flow Join does not require us to sort the input streams first. Unnecessary Sort transformations can add extra processing time.

---

## 7. QUICK REVISION TABLE

| Concept | Simple meaning |
|---|---|
| Mapping Data Flow | Visual Spark-based transformation |
| Source | Reads incoming data |
| Transformation | Processes the data |
| Sink | Writes final output |
| Projection | Column and data type blueprint |
| Schema Drift | Handles changing source schemas |
| Debug Mode | Tests Data Flows using debug compute |
| Data Preview | Shows data at a transformation |
| Select | Chooses and modifies columns |
| Derived Column | Creates or changes columns |
| Filter | Removes unwanted rows |
| Join | Combines two streams |
| Aggregate | Groups records and calculates summaries |
| Window | Calculates over related rows |
| Pivot | Rows into columns |
| Unpivot | Columns into rows |
| Surrogate Key | Artificial key for records |
| Exists | Checks whether a match exists |
| Lookup | Finds matching reference information |
| Conditional Split | Divides records based on conditions |
| Flowlet | Reusable transformation logic |
| SCD Type 1 | Overwrites old values |
| SCD Type 2 | Preserves history |
| TTL | Controls how long eligible compute stays available |
| PolyBase | Supports bulk loading into Synapse |
| CDC Checkpoint | Remembers change-processing progress |
| Data Skew | Uneven data distribution |
| OOM | Not enough memory |
| Join Explosion | Unexpected increase in Join output |

---

## 8. IMPORTANT DOCUMENTATION AND LEARNING LINKS

### Official Microsoft documentation

1. [Mapping Data Flow Overview](https://learn.microsoft.com/en-us/azure/data-factory/concepts-data-flow-overview)
2. [Execute Data Flow Activity](https://learn.microsoft.com/en-us/azure/data-factory/control-flow-execute-data-flow-activity)
3. [Source Transformation](https://learn.microsoft.com/en-us/azure/data-factory/data-flow-source)
4. [Mapping Data Flow Debug Mode](https://learn.microsoft.com/en-us/azure/data-factory/concepts-data-flow-debug-mode)
5. [Schema Drift](https://learn.microsoft.com/en-us/azure/data-factory/concepts-data-flow-schema-drift)
6. [Transformation Overview](https://learn.microsoft.com/en-us/azure/data-factory/data-flow-transformation-overview)
7. [Data Flow Monitoring](https://learn.microsoft.com/en-us/azure/data-factory/concepts-data-flow-monitoring)
8. [Data Flow Performance and Tuning](https://learn.microsoft.com/en-us/azure/data-factory/concepts-data-flow-performance)
9. [Troubleshoot Mapping Data Flows](https://learn.microsoft.com/en-us/azure/data-factory/data-flow-troubleshoot-guide)
10. [Data Flow Expression Functions](https://learn.microsoft.com/en-us/azure/data-factory/data-flow-expression-functions)
11. [Delimited Text Format](https://learn.microsoft.com/en-us/azure/data-factory/format-delimited-text)
12. [Sink Transformation](https://learn.microsoft.com/en-us/azure/data-factory/data-flow-sink)

### Additional learning resources you shared

- [Datasets vs Inline Datasets in ADF](https://mohan-balaji.medium.com/datasets-vs-inline-data-in-azure-data-factory-for-seamless-data-integration-3dee1c27c4da)
- [Window, Pivot, Unpivot, Surrogate Key, Exists and Lookup](https://youtu.be/x4rgruCphpU?si=4g56EIkeV__YN5rW)
- [Conditional Split Transformation](https://youtu.be/qyfZXvmYGFo?si=Ik-iHRStOw1gPLg)
- [Additional Data Flow Learning Video](https://youtu.be/faRuXo6VaDo?si=gnsDvHUTZ3dcwZUb)

---

## FINAL THOUGHT – HOW TO THINK LIKE A DATA ENGINEER

When you build a Mapping Data Flow, don't just think about which transformation to drag and drop.

Always ask:

1. Where is my data coming from?
2. What is the structure of the source data?
3. What changes do I need to make?
4. How do I check whether my output is correct?
5. Where should I store the final data?
6. If the Data Flow fails, where should I start debugging?
7. If it becomes slow, how can I identify the actual bottleneck?

**The main skill is not memorizing transformation names. It is understanding how data moves, how it changes, and how to find problems when something goes wrong.**