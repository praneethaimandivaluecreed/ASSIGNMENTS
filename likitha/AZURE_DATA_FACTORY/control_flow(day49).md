# Azure Data Factory – Control Flow Activities

## 1. What is Control Flow in ADF?

Control Flow defines **how, when, and under what conditions activities execute inside an ADF pipeline.**

For example, consider a requirement to copy multiple files from Azure Blob Storage to ADLS.

We need to:
1. Find the available files.
2. Get their names and details.
3. Loop through the files.
4. Copy each file.
5. Check whether the copy succeeded.
6. Handle failures if they occur.

Control Flow activities help us design this execution logic.

---

## 2. Basic Control Flow Activities

### 2.1 Lookup Activity

**Purpose:** Retrieves data or records from a source, such as a SQL table or file, so that subsequent activities can use them.

Example: Retrieve the list of tables that need to be copied.

```sql
SELECT TableName FROM TableConfiguration;
```

The Lookup output (with `firstRowOnly = false`) looks like:

```json
{
  "count": 3,
  "value": [
    {"TableName": "Employees"},
    {"TableName": "Customers"},
    {"TableName": "Orders"}
  ]
}
```

To pass the complete array into ForEach:

```adf
@activity('LookupTables').output.value
```

**Important points:**
- `firstRowOnly = true` returns one row under `output.firstRow`.
- `firstRowOnly = false` returns multiple rows under `output.value`.
- Maximum output: 5,000 rows and 4 MB.
- Use Lookup mainly to retrieve metadata, configuration and small result sets, not large datasets.

### 2.2 Get Metadata Activity

**Purpose:** Retrieves information (metadata) about a file, folder or dataset without reading its actual data.

Example: Check whether a file exists and get its details.

Common metadata fields:

| Field | Purpose |
|---|---|
| exists | Checks whether the file/folder exists |
| name | Gets the file or folder name |
| size | Gets file size |
| lastModified | Gets last modified date |
| childItems | Gets files and folders inside a folder |
| structure | Gets the structure of a supported dataset |

Example: To list files inside a folder, select `childItems`.

**Lookup vs Get Metadata:**

- Lookup retrieves data/records from a source.
- Get Metadata retrieves information about a file, folder or dataset.
- Lookup can return table records; Get Metadata can return file properties and folder contents.

### 2.3 Set Variable Activity

**Purpose:** Assigns a value to an existing pipeline variable.

Example:

```adf
@activity('LookupTables').output.count
```

We can store the Lookup count in an Integer variable named `TotalTables`.

Variables are useful for maintaining temporary values during pipeline execution.

**Important:** ADF does not allow a variable to reference itself in its own Set Variable expression.

For example, this is invalid:

```adf
@variables('Counter') + 1
```

To increment a variable, use a temporary variable or another supported expression approach.

### 2.4 Append Variable Activity

**Purpose:** Adds a new value to an existing Array variable without replacing its existing contents.

Example:

Initial array:

```json
["Employees"]
```

Append:

```text
Customers
```

Result:

```json
["Employees", "Customers"]
```

**Set Variable vs Append Variable:**
- Set Variable replaces the variable's value.
- Append Variable adds an element to an existing array.

**Important concurrency point:** Pipeline variables are shared at pipeline scope. Updating them inside parallel ForEach iterations can cause unexpected results because multiple iterations may update the same variable simultaneously.

### 2.5 Filter Activity

**Purpose:** Filters an input array based on a condition and returns only the matching elements.

Example:

Input:

```json
["employees.csv", "orders.txt", "customers.csv"]
```

Condition: Keep only CSV files.

Output:

```json
["employees.csv", "customers.csv"]
```

The Filter activity uses:
- Items: Input array.
- Condition: Boolean expression deciding which elements to retain.

Example condition:

```adf
@endsWith(item(), '.csv')
```

**Remember:**
- Filter changes the contents/size of an array.
- If Condition makes a business decision based on a condition.

A useful rule: Use Filter to select items from an array; use If Condition to decide which execution path to follow.

---

## 3. Control Flow Activities for Decision-Making and Loops

### 3.1 ForEach Activity

**Purpose:** Executes activities repeatedly for each element in an input array.

Example:

```adf
@activity('LookupTables').output.value
```

Inside ForEach:

```adf
@item().TableName
```

`item()` represents the current element being processed.

**Sequential vs Parallel:**

| Sequential | Parallel |
|---|---|
| One iteration at a time | Multiple iterations simultaneously |
| Slower for independent tasks | Faster when resources allow |
| Easier to control shared operations | Needs concurrency management |
| Useful when tasks depend on each other | Useful when tasks are independent |

Important properties:
- `isSequential = true`: Executes one iteration at a time.
- `isSequential = false`: Allows parallel execution.
- `batchCount`: Maximum number of concurrent iterations.
- Default batchCount = 20; maximum = 50.
- Maximum total ForEach items = 100,000.

**Concurrency warning:** If multiple iterations write to the same destination file, they can cause conflicts. Parallel execution should be used carefully.

Also, Set Variable and Append Variable operations inside parallel loops can cause race conditions because pipeline variables are shared.

### 3.2 If Condition Activity

**Purpose:** Executes one of two branches based on a Boolean condition.

It has:
- True branch
- False branch

Example: Check whether a file exists.

```adf
@activity('GetMetadata').output.exists
```

If True → Copy the file.

If False → Log that the file is missing.

### 3.3 Switch Activity

**Purpose:** Selects one execution branch from multiple possible cases based on an expression.

Example: Choose the processing logic based on file type.

```text
.csv → CSV processing
.json → JSON processing
.parquet → Parquet processing
```

Important points:
- At least one case is required.
- Maximum 25 cases.
- Default case handles values that do not match any configured case.

**If vs Switch:**
- If Condition is useful for True/False decisions.
- Switch is useful when there are multiple possible values or execution paths.

### 3.4 Until Activity

**Purpose:** Repeats activities until a specified condition becomes True.

Example: Wait until a file is available.

```text
Check file exists
       ↓
Is file available?
   No → Wait → Check again
   Yes → Exit loop
```

Important points:
- Until checks its exit condition after executing its inner activities.
- It is useful for polling, such as checking whether a file or another process is ready.
- Configure a timeout to prevent endless execution.
- Default timeout is 7 days; maximum is 90 days.
- A failed inner activity does not mean the Until condition has automatically become True. Handle errors explicitly.

### 3.5 Wait Activity

**Purpose:** Pauses pipeline execution for a specified duration.

Example: Wait for 30 seconds before checking whether a file has arrived.

**Polling vs Throttling:**
- Polling means repeatedly checking something, such as whether a file is ready.
- Throttling means deliberately controlling how frequently checks or requests happen to avoid overwhelming a system.
- Wait can be used to introduce a delay between polling attempts.

---

## 4. Execute Pipeline Activity – Reusable Child Pipelines

**Purpose:** Calls another pipeline from the current pipeline.

Instead of putting every processing step inside a ForEach loop, we can create a separate child pipeline and invoke it using Execute Pipeline.

Example:

Parent pipeline:
1. Lookup departments.
2. ForEach through departments.
3. Execute the child pipeline and pass the current department.

Child pipeline:
1. Receive DepartmentName.
2. Retrieve files for that department.
3. Process the files.

### Passing parameters

Parent passes values using the Execute Pipeline activity's parameters property.

Example:

```adf
@item().DepartmentName
```

Child receives the value through:

```adf
@pipeline().parameters.DepartmentName
```

**Important concepts:**

- Parent and child pipelines have separate variable scopes.
- Child pipelines cannot directly access or modify the parent's variables.
- Values must be explicitly passed using parameters.
- If the child needs to send a result back, use Set Pipeline Return Value and retrieve the returned value through the supported pipeline activity output.
- `waitOnCompletion = true` by default. The parent waits until the child pipeline finishes.
- If set to false, the parent does not wait for the child to finish.

**Array-to-string catch:** Passing an array through pipeline parameter mapping may result in the child receiving a string representation rather than a native array. Check the actual parameter value and convert/parse it appropriately before using it in a ForEach.

**Nested loop limitation:** A ForEach or Until cannot be directly nested inside another ForEach or Until. Use separate parent and child pipelines with Execute Pipeline to structure such processing.

---

## 5. Dependency Lines – How ADF Decides What Runs

Dependency lines decide when a downstream activity is allowed to execute based on the previous activity's status.

ADF supports four dependency conditions:

| Condition | Meaning |
|---|---|
| Upon Success | Runs only if the previous activity succeeds |
| Upon Failure | Runs only if the previous activity fails |
| Upon Completion | Runs after the previous activity finishes, whether successful or failed |
| Upon Skip | Runs if the previous activity is skipped |

### Example 1: Upon Success

```text
CopyData → Success → ValidateData
```

If CopyData succeeds, ValidateData runs.

If CopyData fails, ValidateData is skipped.

### Example 2: Upon Failure

```text
CopyData → Failure → ErrorLogger
```

If CopyData fails, ErrorLogger runs.

If CopyData succeeds, ErrorLogger is skipped.

### Example 3: Upon Completion

```text
CopyData → Completion → Cleanup
```

Cleanup runs whether CopyData succeeds or fails.

### Example 4: Upon Skip

If the previous activity is skipped, the downstream activity configured with Upon Skip can execute.

### Important: Understanding Skipped and Pipeline Status

A skipped activity does not automatically mean the entire pipeline failed.

ADF evaluates the dependency chain. When an activity is skipped, its upstream parent's outcome is considered in determining the overall pipeline result.

For example:

```text
CopyData → Upon Failure → ErrorLogger
```

If CopyData succeeds:
- CopyData = Succeeded
- ErrorLogger = Skipped
- Overall pipeline can still be Succeeded.

The skipped error-handling branch is expected because its failure condition was not met.

**Multiple dependencies:** If two activities are connected to one downstream activity using Upon Success, that downstream activity waits for both dependencies to succeed. If either fails, the downstream activity is skipped.

### Important error-handling pattern

Suppose two independent activities, A and B, must both succeed before continuing.

A useful pattern is:

```text
Activity A ── Upon Completion ──┐
                                ↓
                            If Condition
                                ↓
Activity B ── Upon Completion ──┘
```

Condition:

```adf
@and(
  equals(activity('A').Status, 'Succeeded'),
  equals(activity('B').Status, 'Succeeded')
)
```

- True branch: Both activities succeeded.
- False branch: At least one activity failed; perform error logging.

This allows a central error-handling branch instead of relying only on direct Upon Failure dependencies.

**Note:** Handled errors can be logged without necessarily failing the overall pipeline. However, if the failure must remain visible as a failed pipeline run, explicitly preserve or re-raise the failure after logging.

---

## 6. Debugging Control Flow Activities

### 6.1 ForEach iteration failures

If one iteration fails:
1. Open Monitor → Pipeline runs.
2. Open the failed pipeline run.
3. Open the ForEach activity's iteration details.
4. Identify the failed iteration.
5. Open its child activity.
6. Inspect Input, Output and error message.
7. Identify the root cause and fix it.

Possible causes:
- Missing source file.
- Incorrect folder or file path.
- Authentication or permission issues.
- Incorrect dataset parameter mapping.
- Parallel execution and resource contention.

Do not assume that the entire ForEach configuration is wrong just because one iteration failed.

### 6.2 Activity Skipped

Skipped means the activity did not execute because its dependency condition was not satisfied.

Example:

```text
CopyData → Failed
     ↓
ValidateData → Skipped
```

If ValidateData requires CopyData to succeed, it will be skipped.

**Debugging:** Check the skipped activity's upstream dependency and the upstream activity's status. Do not treat every Skipped status as an error.

### 6.3 Output size limits

Important limits:

| Activity / operation | Limit |
|---|---|
| Lookup maximum rows | 5,000 |
| Lookup output size | 4 MB |
| Web activity output | Around 4 MB |
| Activity input/configuration payload | 896 KB |
| ForEach total items | 100,000 |

If Lookup exceeds its limits:
- Retrieve only required columns.
- Split records into smaller batches.
- Use Copy activity to move large data into storage.
- Pass file paths, table names or IDs instead of large datasets.

Remember: The Lookup output limit is not a limit on how much data Copy activity can move.

For more than 100,000 ForEach items, use a batched parent-child pipeline design.

### 6.4 Wrong item() reference

`@item()` returns the current item inside ForEach.

If the current item is a string:

```adf
@item()
```

If the current item is an object:

```json
{
  "FileName": "employees.csv",
  "FolderName": "HR"
}
```

Use:

```adf
@item().FileName
```

To get the folder:

```adf
@item().FolderName
```

Common mistakes:
- Using `@item().FileName` when the item is actually a string.
- Using `@item()` when the dataset expects a filename string but receives an entire object.
- Using the wrong property name.
- Using `item()` outside a ForEach context.

**Debugging tip:** Always inspect the actual Lookup output and ForEach input JSON before writing expressions.

---

## 7. Read Each Iteration's Input and Output in Monitor

This is an important practical debugging skill.

When a ForEach activity fails, do not inspect only its parent activity.

Follow this path:

```text
Monitor
   ↓
Pipeline runs
   ↓
Open pipeline run
   ↓
Open ForEach activity
   ↓
View iteration details
   ↓
Select the failed iteration
   ↓
Open child activity
   ↓
Inspect Input and Output
```

**Input tab:** Shows the evaluated values passed to the activity.

Check:
- Current filename.
- Folder path.
- Dataset parameters.
- Source and destination configuration.
- Evaluated dynamic expressions.

**Output tab:** Shows execution results, including available details such as:
- Activity status.
- Rows read and written.
- Data copied.
- Execution details.
- Error code and error message.

Example:

```text
Iteration 1 → employees.csv → Succeeded
Iteration 2 → customers.csv → Succeeded
Iteration 3 → orders.csv → Failed
```

Open iteration 3 and inspect the Copy activity's Input and Output to identify why orders.csv failed.

**Important:** The expression editor shows what you wrote. Monitor's Input JSON shows what ADF actually evaluated and passed to the activity.

---

## 8. Quick Revision – Important Points

1. Lookup retrieves records; Get Metadata retrieves file/dataset information.
2. Set Variable replaces a value; Append Variable adds an element to an array.
3. Filter selects elements from an array; If Condition makes a True/False decision.
4. ForEach processes an array sequentially or in parallel.
5. `batchCount` controls maximum concurrent iterations (maximum 50).
6. ForEach supports up to 100,000 total items.
7. Switch selects among multiple cases (maximum 25).
8. Until repeats activities until its condition becomes True.
9. Wait pauses execution for a specified duration.
10. Execute Pipeline calls reusable child pipelines.
11. Parent and child variables are isolated; pass values through parameters.
12. Dependencies determine whether downstream activities run or get skipped.
13. Skipped does not automatically mean pipeline failure.
14. Lookup supports a maximum of 5,000 rows and 4 MB output.
15. `@item()` represents the current ForEach element.
16. Monitor → iteration → Input/Output is essential for debugging.

---

## 9. References

### Microsoft Official Documentation

1. [ForEach activity](https://learn.microsoft.com/en-us/azure/data-factory/control-flow-for-each-activity)
2. [Execute Pipeline activity](https://learn.microsoft.com/en-us/azure/data-factory/control-flow-execute-pipeline-activity)
3. [Set Variable activity](https://learn.microsoft.com/en-us/azure/data-factory/control-flow-set-variable-activity)
4. [Pipeline failure and error handling](https://learn.microsoft.com/en-us/azure/data-factory/tutorial-pipeline-failure-error-handling)
5. [Pipeline return value](https://learn.microsoft.com/en-us/azure/data-factory/tutorial-pipeline-return-value)

### Additional Learning References

6. [Get Metadata vs Lookup activity – Medium](https://medium.com/@rganesh0203/get-metadata-vs-lookup-activity-in-azure-data-factory-azure-synapse-analytics-9eacd6d2e843)
7. [Azure Data Factory discussion – ForEach failure and error handling](https://techcommunity.microsoft.com/discussions/azuredatafactory/azure-data-factory-foreach-loop-fails-despite-inner-activity-error-handling---se/4434806)
8. [ADF Control Flow video](https://youtu.be/f9Tq5fIY0vY?si=NCNl44Qd3LQfbLj_)

**Final learning principle:** Control Flow is not just about connecting activities. It is about controlling execution, managing dependencies, handling failures, processing data in batches and making pipelines reusable and reliable.