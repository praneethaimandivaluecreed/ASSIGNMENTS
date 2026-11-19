# AZURE DATA FACTORY
## PAGE 1 – INTRODUCTION TO CALLING EXTERNAL SERVICES

### 1. What does calling external services mean?

Azure Data Factory (ADF) is mainly an orchestration tool. It controls the execution of a data pipeline, but sometimes the actual work needs to be performed by another service.

For example:
- SQL databases can execute SQL queries and stored procedures.
- Databricks can perform large-scale data transformations.
- Azure Functions can execute custom Python or other supported code.
- REST APIs can provide data or perform operations.

ADF connects to these services, sends the required inputs, triggers their execution, and collects their outputs.

**Example:**

Imagine we are building a customer data pipeline.

1. ADF extracts customer data.
2. ADF calls a Databricks notebook to clean the data.
3. Databricks performs the transformations.
4. Databricks returns a status to ADF.
5. ADF continues with the next activity.

Here, ADF controls the workflow, while Databricks performs the processing.

### 2. What is a Linked Service?

A Linked Service is the connection information that allows ADF to connect to an external service or data store.

Examples:
- Azure SQL Linked Service – connects to Azure SQL Database.
- Azure Databricks Linked Service – connects to a Databricks workspace.
- Azure Function Linked Service – connects to an Azure Function App.

**Remember:**

Linked Service = How ADF connects to the service.

Activity = What ADF asks the service to do.

### 3. Integration Runtime (IR) and private connectivity

Integration Runtime helps ADF connect to data stores and compute services.

There are two important options:

**Azure Integration Runtime (Azure IR)**

- Used when the data source or service is publicly accessible over the internet or reachable through supported Azure networking.
- Microsoft manages the infrastructure.
- Commonly used with Azure cloud services and public endpoints.

**Self-Hosted Integration Runtime (SHIR)**

- Used when a data source is inside a private network and cannot be reached directly from the public internet.
- Installed on a machine inside that private network.
- Acts as a secure bridge between ADF and the private data source.

Example: If a SQL Server database is running on a company computer behind a firewall, SHIR can help ADF communicate with it.

---

## PAGE 2 – STORED PROCEDURE ACTIVITY

### 1. What is a Stored Procedure?

A Stored Procedure is a collection of SQL statements stored inside a database. We can execute it whenever we need it instead of writing the same SQL code repeatedly.

Example:

```sql
CREATE PROCEDURE CleanCustomers
AS
BEGIN
    DELETE FROM Customers
    WHERE Email IS NULL;
END;
```

Whenever we execute this procedure, it removes customer records whose email is NULL.

### 2. What is Stored Procedure Activity in ADF?

Stored Procedure Activity allows ADF to execute an already-created stored procedure inside a supported database.

**How to use it:**

1. Create an ADF pipeline.
2. Add Stored Procedure Activity.
3. Select the SQL Linked Service.
4. Choose the stored procedure.
5. Provide the required input parameters.
6. Run or debug the pipeline.

ADF invokes the procedure, and the database executes the SQL code.

### 3. Where is Stored Procedure Activity supported?

In the connector context covered in this syllabus, the main supported databases are:

- Azure SQL Database
- SQL Server
- Azure Synapse Analytics

It is not a universal activity for every database. For example, do not assume that this activity directly supports PostgreSQL, Oracle, or ADLS.

### 4. Passing parameters to a Stored Procedure

Suppose the stored procedure accepts a customer ID.

```sql
CREATE PROCEDURE GetCustomer
    @CustomerId INT
AS
BEGIN
    SELECT * FROM Customers
    WHERE CustomerId = @CustomerId;
END;
```

Instead of hardcoding the customer ID, we can pass it dynamically from ADF.

**Steps:**

1. Create a pipeline parameter named `customer_id`.
2. In Stored Procedure Activity, select the procedure.
3. Add its parameter and map it to the pipeline parameter.
4. Use this expression:

```text
@pipeline().parameters.customer_id
```

5. During debugging, provide a value such as `101`.

ADF passes the value to the stored procedure.

**Important distinction:**

- Pipeline parameter: Holds the value at pipeline level.
- Stored procedure parameter: Receives the value inside SQL.
- Dynamic expression: Connects the two.

### 5. Passing NULL and parameter types

When passing a NULL value in JSON, write it in lowercase:

```json
{
  "param1": {
    "value": null
  }
}
```

The word `null` is a JSON value, not a string.

ADF parameter types such as `Int` are ADF service types. ADF maps them to the appropriate database types supported by the connector.

### 6. Stored Procedure in Copy Activity

Copy Activity also supports stored procedures in certain source and sink scenarios.

**A. Source-side stored procedure**

Property: `sqlReaderStoredProcedureName`

Purpose:
- Execute a stored procedure before reading data.
- Filter rows inside the database.
- Join or prepare data before ADF copies it.

Example: Instead of copying every customer record, the stored procedure returns only customers added today.

**B. Sink-side stored procedure**

Property: `sqlWriterStoredProcedureName`

Purpose:
- Execute a stored procedure while writing copied data.
- Perform operations such as UPSERT (Update + Insert).
- Validate or merge incoming records.

Example: Before inserting a customer, the stored procedure checks whether that customer already exists.

**Important support distinction:**

- Source-side stored procedure: Supported in the relevant Azure SQL Database, SQL Server, and Azure Synapse scenarios.
- Sink-side stored procedure: Supported for Azure SQL Database and SQL Server, but not Azure Synapse Analytics in this Copy Activity scenario.

For writing into Azure Synapse, use a separate Stored Procedure Activity when you need to execute a stored procedure after the Copy Activity.

### 7. Stored Procedure Activity vs Copy Activity

| Stored Procedure Activity | Copy Activity |
|---|---|
| Executes a stored procedure | Moves data from source to sink |
| Used for database-side SQL operations | Used for data movement |
| Can run a procedure directly | Can use stored procedures in supported source/sink scenarios |

**Important limitation: Stored Procedure output**

Do not assume that Stored Procedure Activity can return every kind of SQL output or result set to ADF.

If you need to retrieve rows or output values, consider Lookup Activity or Script Activity, depending on the SQL operation and required output.

An SQL error code such as 201 can indicate that a required procedure parameter was not supplied. It is not automatically proof that every stored procedure with output parameters will fail.

---

## PAGE 3 – SCRIPT ACTIVITY

### 1. What is Script Activity?

Script Activity allows us to execute SQL scripts directly from an ADF pipeline.

It is useful when we want to perform SQL operations without creating a separate Stored Procedure for every task.

### 2. What can we do using Script Activity?

Common use cases:

- Truncate a table before loading fresh data.
- Create, alter, or drop tables and views.
- Re-create fact and dimension tables.
- Execute INSERT, UPDATE, and DELETE statements.
- Execute stored procedures.
- Run SELECT queries and retrieve result sets.
- Perform database preparation tasks before loading data.

Example:

```sql
TRUNCATE TABLE Customers;
```

This removes all rows from the Customers table while keeping its structure.

### 3. Supported data stores

Script Activity supports several data stores, including:

- Azure SQL Database
- SQL Server
- Azure Synapse Analytics
- Oracle
- Snowflake
- SQL Managed Instance

Always check the connector's current support and limitations before using it.

### 4. Query vs NonQuery

This is an important Script Activity concept.

**A. Query (default)**

Used when the SQL statement returns rows.

Example:

```sql
SELECT * FROM Customers;
```

ADF returns the rows in the activity output under `resultSets`.

The output also includes `resultSetCount`.

**B. NonQuery**

Used when the SQL statement performs an action but does not return a result set.

Examples:

```sql
INSERT INTO Customers
VALUES (101, 'Likhita');

UPDATE Customers
SET Name = 'Likhita'
WHERE CustomerId = 101;

DELETE FROM Customers
WHERE CustomerId = 101;
```

For NonQuery, the activity output includes:

`recordsAffected` – the number of rows affected by the operation.

### 5. Parameter directions

Unlike the Stored Procedure Activity, Script Activity supports different parameter directions:

- Input: ADF sends a value to SQL.
- Output: SQL returns a value to ADF.
- InputOutput: ADF sends a value, and SQL can modify and return it.

**Important points:**

- If direction is Output, the initial value provided is ignored.
- ReturnValue is not supported as a parameter direction.
- If a stored procedure has a return value, assign that value to an Output parameter if you need to retrieve it.
- The `size` property applies to Output or InputOutput parameters of type string or byte array.

### 6. Using Script Activity to retrieve stored procedure results

Suppose a stored procedure returns customer details.

We can call it through Script Activity using a Query script.

Example:

```sql
EXEC dbo.GetCustomers;
```

If the stored procedure returns results from a temporary table, use `WITH RESULT SETS` to define the expected result metadata when required.

Example:

```sql
EXEC dbo.GetCustomerDetails
WITH RESULT SETS
(
    (
        Id INT,
        Name NVARCHAR(100)
    )
);
```

This tells ADF what columns and data types to expect from the returned result set.

### 7. Script Activity output limitations

The activity output can contain up to:

- 5,000 rows
- 4 MB of data

If the output exceeds these limits, ADF may truncate the output. The `outputTruncated` property indicates truncation.

**Remember:** Do not use Script Activity output to transfer millions of rows. Use it for smaller query results and status information.

### 8. Logging

When logging is enabled, print or logging statements from supported script execution can appear in the activity output logs.

This helps us understand what happened during script execution.

### 9. Stored Procedure vs Script Activity

| Stored Procedure Activity | Script Activity |
|---|---|
| Executes a stored procedure | Executes SQL scripts |
| Useful for existing reusable procedures | Useful for direct SQL operations |
| Limited output capabilities | Supports Query results and Output/InputOutput parameters |
| Best when logic is already stored in the database | Best when we need flexible SQL execution |

---

## PAGE 4 – DATABRICKS NOTEBOOK ACTIVITY

### 1. What is Notebook Activity?

Notebook Activity allows ADF to execute a notebook in an external compute service such as:

- Azure Databricks
- Azure Synapse Analytics

A notebook can contain Python, SQL, Scala, or other supported code depending on the platform.

ADF is responsible for triggering the notebook. The notebook performs the actual data processing.

### 2. How to configure Databricks Notebook Activity

Steps:

1. Create an ADF pipeline.
2. Add a Databricks Notebook Activity.
3. Create a Databricks Linked Service.
4. Configure the workspace connection and authentication.
5. Select the notebook path.
6. Configure the required compute settings.
7. Pass pipeline parameters through Base parameters.
8. Run or debug the pipeline.

**Important distinction:**

- Linked Service: Connects ADF to Databricks.
- Notebook path: Identifies which notebook should execute.
- Compute/cluster: Provides the resources to run the notebook.
- Base parameters: Pass input values from ADF to the notebook.

### 3. Passing parameters from ADF to Databricks

Suppose the notebook needs a file name.

**Step 1: Create a pipeline parameter**

```text
file_name
```

**Step 2: Open Notebook Activity → Settings → Base parameters**

Map:

```text
file_name → @pipeline().parameters.file_name
```

**Step 3: Receive the parameter inside Databricks**

```python
file_name = dbutils.widgets.get("file_name")

print(file_name)
```

The notebook receives the value sent by ADF.

**Understand the complete flow:**

ADF pipeline parameter → Notebook Activity Base parameter → Databricks widget → `dbutils.widgets.get()`.

### 4. Returning output from Databricks to ADF

Sometimes the notebook completes a task and needs to send a result back to ADF.

For example, it may return:

`Data processing completed successfully`

Inside the notebook:

```python
result = "Data processing completed successfully"

dbutils.notebook.exit(result)
```

ADF captures this returned value in the Notebook Activity output.

Suppose the activity name is `RunNotebook`.

Use this expression:

```text
@activity('RunNotebook').output.runOutput
```

We can use this output in:

- Set Variable Activity
- If Condition Activity
- Another Notebook Activity
- Web Activity

**Important limitation:**

`runOutput` has a 2 MB size limit. Do not try to return an entire DataFrame or millions of records.

Return small values such as:
- Success or failure status
- Number of processed records
- Output file path
- Short messages

### 5. What happens when two notebooks run simultaneously?

Suppose two ADF pipeline runs execute the same notebook at the same time.

They can execute independently, especially when they use separate job clusters.

However, conflicts can happen if both notebooks write to the same output location.

To avoid this:
- Use separate output paths when appropriate.
- Use safe write strategies.
- Apply concurrency controls when required.

### 6. Debugging Notebook Activity

Common problems:

**Authentication error (401/403):**
- Check the Linked Service authentication.
- Verify permissions to access the workspace.

**Notebook not found:**
- Check the notebook path.
- Verify the selected workspace.

**Parameters not arriving:**
- Check Base parameters.
- Check pipeline parameter expressions.
- Verify the widget name inside the notebook.

**Notebook execution is slow:**
- Inspect Databricks compute and Spark execution.
- Check for expensive transformations, data skew, and slow stages.

**Notebook fails:**
- Inspect the ADF activity error.
- Open Databricks notebook/job logs for detailed errors.

**Remember:** ADF Monitor shows pipeline-level execution. Databricks monitoring and Spark UI help investigate actual notebook and Spark execution.

---

## PAGE 5 – AZURE FUNCTION ACTIVITY AND WEB ACTIVITY

### 1. What is Azure Function Activity?

Azure Function Activity allows ADF to call an HTTP-triggered Azure Function.

Azure Functions are serverless compute services that allow us to execute custom code without managing the underlying servers.

We can use them for:
- Custom business logic.
- Data validation.
- Calling external APIs.
- Small processing tasks.
- Operations that are not directly available as standard ADF activities.

### 2. Understand the basic terms

**Function App:** The hosting environment that contains Azure Functions.

**Function:** The actual code that performs a task.

**HTTP Trigger:** A trigger that executes the function when it receives an HTTP request.

**Function Key:** An authentication key that can be used to authorize calls to a function.

### 3. How does ADF call an Azure Function?

Steps:

1. Create an Azure Function App.
2. Create a function with an HTTP trigger.
3. Deploy the function.
4. Create an Azure Function Linked Service in ADF.
5. Configure the Function App URL and authentication.
6. Add Azure Function Activity to the pipeline.
7. Select the function and configure the required request details.
8. Pass the required input and execute the pipeline.

Depending on the configuration, authentication can use a function key or Managed Identity.

### 4. Passing parameters to an Azure Function

Suppose ADF needs to send a customer ID.

Request body:

```json
{
  "customer_id": 101,
  "email": "customer@example.com"
}
```

Inside the Python Azure Function:

```python
data = req.get_json()

customer_id = data.get("customer_id")
email = data.get("email")
```

The function reads the JSON request body and extracts the values.

### 5. Returning output from an Azure Function

The function can return a JSON response.

Example:

```json
{
  "customer_id": 101,
  "status": "VALID"
}
```

ADF can capture the response in the activity output.

We can use the returned values in downstream activities by checking the actual Output JSON in ADF Monitor and using the correct dynamic expression.

**Very important limitation:**

ADF Azure Function Activity expects a valid JSON object (JObject) as its response.

Returning a plain string, an array, or an incompatible response can cause an error such as:

`Response Content isn't a valid JObject`

Therefore, design the function to return a JSON object.

### 6. What is Web Activity?

Web Activity allows ADF to call an external HTTP endpoint.

It is useful for:
- Calling REST APIs.
- Sending HTTP requests.
- Starting external jobs.
- Checking job status.
- Calling web services.

It can send HTTP methods such as GET and POST, along with the required headers and body.

### 7. Azure Function Activity vs Web Activity

| Azure Function Activity | Web Activity |
|---|---|
| Designed to call Azure Functions | Designed to call HTTP endpoints |
| Connects to an Azure Function App | Calls a URL |
| Useful for custom serverless code | Useful for APIs and web services |

**Simple example:**

If I want to execute my custom Python function hosted in Azure, I can use Azure Function Activity.

If I want to call an external REST API to get customer details, I can use Web Activity.

---

## PAGE 6 – ASYNCHRONOUS EXECUTION, UNTIL POLLING AND DURABLE FUNCTIONS

### 1. What is asynchronous execution?

Normally, when ADF calls an external service, it may wait for the service to finish and return a response.

But some tasks take a long time.

Instead of keeping the original request waiting, we can start the task and receive an immediate response saying that the task has started.

This approach is called asynchronous execution.

**Example:**

ADF starts a job to process 10 lakh customer records.

The external service immediately responds:

```json
{
  "job_id": "JOB101",
  "status": "Running"
}
```

The actual processing continues in the background.

### 2. What is polling?

Polling means repeatedly checking whether a long-running task has completed.

For example:

1. ADF starts an external job.
2. The service returns a job ID.
3. ADF checks the job status.
4. The status is still Running.
5. ADF waits for some time.
6. ADF checks again.
7. The status becomes Completed.

This repeated checking is called polling.

### 3. Polling using Until Activity

ADF provides Until Activity to implement this pattern.

Example:

Suppose we have an external job that takes 10 minutes.

**Pipeline flow:**

1. Web Activity starts the job.
2. Store the returned Job ID or status URL.
3. Until Activity starts.
4. Inside Until, Web Activity checks the job status.
5. If status is Running, Wait Activity pauses for some time.
6. The loop checks again.
7. When the status becomes Completed, the Until activity exits.
8. ADF continues with the next activity.

**Remember:**

- Asynchronous execution = Starting a task without waiting for it to finish immediately.
- Polling = Repeatedly checking its status.
- Until Activity = ADF activity used to implement repeated polling.

### 4. What are Durable Functions?

Normal Azure Functions are commonly used for individual tasks. They are generally stateless, and the developer must manage long-running workflow state separately.

Durable Functions are an extension of Azure Functions that provides built-in orchestration and state management for long-running workflows.

They can:
- Coordinate multiple functions.
- Track completed steps.
- Wait for external events.
- Retry failed activities.
- Resume workflows using persisted state.

### 5. How do Durable Functions work?

Durable Functions commonly have three main components:

**A. Starter Function**

- Starts the Durable workflow.
- Creates a new workflow instance.

**B. Orchestrator Function**

- Controls the sequence of activities.
- Decides which activity should execute next.
- Manages the workflow's progress.

**C. Activity Function**

- Performs the actual work.
- Examples: Read a file, validate customer data, save results.

**Example:**

Starter → Orchestrator → Validate Customers → Save Customers → Workflow Completed.

### 6. Normal Function vs Durable Function

| Normal Azure Function | Durable Function |
|---|---|
| Executes a specific task | Coordinates a workflow |
| Usually handles individual requests | Manages multiple workflow steps |
| Workflow state must be managed separately | Provides durable state management |
| Suitable for shorter operations | Useful for long-running workflows |

**Important understanding:**

Asynchronous execution and Durable Functions are not the same.

- Asynchronous execution is a way of running work without waiting for immediate completion.
- Durable Functions are a specific Azure Functions extension that helps implement and manage long-running workflows.

We can implement asynchronous processing using a normal Azure Function and ADF Until polling. Durable Functions are not compulsory for every asynchronous task.

### 7. How does ADF work with Durable Functions?

1. ADF calls the Starter Function.
2. The Starter Function starts the Durable workflow.
3. The workflow runs through the Orchestrator and Activity Functions.
4. The Starter returns a status URL or workflow instance details.
5. ADF can use Web Activity and Until polling to check the workflow status.
6. Once completed, ADF continues with the next activity.

**Remember:** Durable Functions manage the long-running workflow. ADF can still orchestrate the larger data pipeline.

---

## PAGE 7 – ORCHESTRATION VS TRANSFORMATION AND DEBUGGING

### 1. Orchestration vs Transformation

This topic asks us to identify which work should be handled by ADF and which work should be handled by a data processing engine.

**Orchestration means:**

Controlling what should happen, when it should happen, and what should happen next.

**Transformation means:**

Actually changing, cleaning, combining, and processing data.

### 2. What should ADF do?

ADF should mainly handle orchestration tasks such as:

- Scheduling pipelines.
- Connecting to data sources.
- Copying data between systems.
- Triggering Databricks notebooks.
- Calling Azure Functions and APIs.
- Executing SQL activities.
- Passing parameters.
- Managing dependencies.
- Handling failures and retries.
- Monitoring pipeline execution.

### 3. What should ADF NOT do?

ADF should not be forced to handle heavy and complex data transformations through pipeline control-flow activities.

Examples of heavy processing:

- Joining millions of records.
- Removing duplicates from huge datasets.
- Performing complex aggregations.
- Applying complicated business rules.
- Processing large volumes of data.

Instead, delegate these tasks to an appropriate processing engine.

**Possible processing engines:**

- Mapping Data Flows: Visual data transformations powered by Spark.
- Databricks: Complex processing using Spark, Python, SQL, etc.
- SQL engines: Database-side transformations using SQL.

### 4. Real-world example

Suppose we receive customer, product, and order data.

**ADF responsibilities:**

1. Extract the data.
2. Trigger the transformation engine.
3. Wait for execution to finish.
4. Handle failures.
5. Load the processed data.
6. Monitor the workflow.

**Mapping Data Flow responsibilities:**

1. Remove duplicates.
2. Handle missing values.
3. Join customer and order data.
4. Calculate total customer spending.
5. Apply business rules.
6. Produce the transformed dataset.

**Important:** ADF can perform basic data operations too. For example, Copy Activity moves data and supports mappings, while Filter Activity filters pipeline items. The point is to use the right tool for the complexity and scale of the operation.

### 5. Debugging external service calls

When ADF calls an external service, three important debugging situations can occur.

#### A. Timeout

**Meaning:**

ADF waits for a response from an external service, but the response does not arrive within the allowed time.

Example:

- ADF calls an Azure Function.
- The function starts processing a large file.
- The operation takes 10 minutes.
- The activity's configured timeout is 2 minutes.
- ADF reports a timeout.

**How to debug:**

1. Open ADF Monitor.
2. Find the failed pipeline run.
3. Select the failed activity.
4. Check the error message and execution duration.
5. Check whether the external service is still processing or has failed.

**Possible solutions:**

- Increase the timeout when appropriate and supported.
- Optimize the external service.
- Use asynchronous execution and polling for long-running jobs.

Important: A timeout does not always mean the external service failed. It may still be processing.

#### B. Parameters not arriving

**Meaning:**

ADF sends an input value, but the external service receives NULL, an empty value, or an incorrect value.

Example:

ADF intends to send:

```json
{
  "customer_id": 101
}
```

But the external service receives:

```json
{
  "customer_id": null
}
```

**How to debug:**

1. Open the failed activity in ADF Monitor.
2. Inspect the Activity Input JSON.
3. Verify whether the dynamic expression was evaluated correctly.
4. Check the request body and parameter mapping.
5. Verify whether the external service reads the correct JSON field.

Example Python code:

```python
data = req.get_json()

customer_id = data.get("customer_id")
```

The JSON key must match the key sent by ADF.

**Remember:** Activity Input JSON tells us what ADF sent.

#### C. Reading error output from an external service

**Meaning:**

ADF successfully sends a request, but the external service returns an error.

Example:

```json
{
  "error": "Customer ID is missing",
  "status": 400
}
```

This means the external service rejected the request because the required input was missing.

**How to debug:**

1. Open ADF Monitor.
2. Find the failed activity.
3. Open its Output JSON.
4. Inspect the error message and HTTP status code.
5. Check external service logs if more details are required.

**Common HTTP status codes:**

| Code | Meaning | Possible reason |
|---|---|---|
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Incorrect URL or resource |
| 429 | Too Many Requests | Too many requests sent |
| 500 | Internal Server Error | Problem inside the external service |

**Important:** ADF Output JSON may not contain the complete error details. For deeper investigation, check service logs such as Azure Function Application Insights.

### 6. Three important debugging places

| What we want to investigate | Where to check |
|---|---|
| What did ADF send? | Activity Input JSON |
| What did the service return? | Activity Output JSON |
| What happened inside the service? | External service logs |

**Example viva answer:**

"If parameters are not reaching an external service, I first inspect Activity Input JSON in ADF Monitor to verify whether the dynamic expressions were evaluated correctly. Then I check the request body and the receiving function's parameter mapping."

---

## PAGE 8 – CHAINING PIPELINES SAFELY AND FINAL REVISION

### 1. What is Pipeline Chaining?

Pipeline chaining means executing multiple pipelines in a sequence, where the completion of one pipeline controls the execution of the next pipeline.

ADF provides an activity called **Execute Pipeline** to call one pipeline from another.

**Parent Pipeline:** The main pipeline that controls the workflow.

**Child Pipeline:** A separate pipeline called by the parent pipeline to perform a specific task.

Example:

MasterPipeline:
- ExtractPipeline
- TransformPipeline
- LoadPipeline

### 2. How to chain pipelines?

1. Create a parent pipeline.
2. Add Execute Pipeline Activity.
3. Select the required child pipeline.
4. Configure the child pipeline parameters.
5. Add another Execute Pipeline Activity for the next child pipeline.
6. Connect activities using the required dependency conditions.
7. Debug and monitor the pipeline.

### 3. Wait on Completion

Execute Pipeline Activity has a setting called `Wait on completion`.

**True:**

- Parent pipeline waits until the child pipeline finishes.
- The parent can use the child's completion status to control the next step.
- Useful when the next activity depends on the child pipeline's result.

**False:**

- Parent continues after the child pipeline is started.
- Parent does not wait for the child to finish.
- Useful when the parent does not need to wait for the child result.

For sequential processing, use True when the next step depends on the previous child pipeline.

### 4. Safe pipeline chaining practices

#### A. Use correct dependency conditions

ADF supports dependency conditions:

- Success: Runs when the previous activity succeeds.
- Failure: Runs when the previous activity fails.
- Completion: Runs when the previous activity finishes, whether successful or failed.
- Skipped: Runs when the previous activity is skipped.

Example:

Extract → Success → Transform → Success → Load.

If Transform fails, Load should not execute through the normal success path.

#### B. Handle failures properly

Suppose Extract succeeds but Transform fails.

A safe pipeline should:

1. Stop the normal success path.
2. Capture the error details.
3. Log the failure.
4. Send an alert if required.
5. Avoid loading incomplete or incorrect data.
6. Allow safe recovery after fixing the issue.

#### C. Pass parameters

Instead of hardcoding table names or file names, pass values from the parent pipeline to the child pipeline.

Example:

Parent passes:

```text
table_name = customers
```

Child receives it using:

```text
@pipeline().parameters.table_name
```

This makes child pipelines reusable.

#### D. Prevent duplicate processing (Idempotency)

Idempotency means rerunning the same operation should not create duplicate or incorrect data.

Example:

Suppose a pipeline inserts 5,000 records and then fails. If we rerun it, those same records might be inserted again.

To prevent this:

- Use UPSERT or MERGE where appropriate.
- Use unique keys.
- Maintain watermark or processing tables.
- Use safe write strategies.
- Avoid blindly inserting the same records again.

**Remember:** A retry should not create duplicate data.

#### E. Configure retries and monitor failures

- Configure retry count and retry interval for temporary failures.
- Do not blindly retry permanent errors such as invalid credentials or incorrect SQL syntax.
- Monitor parent and child pipeline runs.
- Check activity errors and execution details in ADF Monitor.

### 5. What happens when a child pipeline fails?

Consider:

MasterPipeline → Extract → Transform → Load.

If Extract succeeds but Transform fails:

- The Execute Pipeline activity for Transform fails.
- The normal Success path should not continue to Load.
- The parent can use Failure dependency to handle the error.
- The failed stage can be rerun after the issue is fixed.

### 6. Final quick revision

| Topic | Important point to remember |
|---|---|
| Stored Procedure Activity | Executes an existing stored procedure in a supported database |
| Copy Activity stored procedure | Can use stored procedures on supported source and sink sides |
| Script Activity | Executes SQL scripts directly |
| Query | Returns rows through resultSets |
| NonQuery | Executes actions and reports recordsAffected |
| Script output limit | 5,000 rows or 4 MB |
| Notebook Activity | Runs Databricks or Synapse notebooks |
| Base parameters | Pass values from ADF to the notebook |
| `dbutils.widgets.get()` | Receives parameters inside Databricks |
| `dbutils.notebook.exit()` | Returns a value from the notebook |
| `runOutput` | Captures the notebook's returned value |
| Azure Function Activity | Calls an HTTP-triggered Azure Function |
| Web Activity | Calls an HTTP endpoint or REST API |
| Async execution | Starts work without waiting for immediate completion |
| Polling | Repeatedly checks job status |
| Until Activity | Implements repeated polling |
| Durable Functions | Manages long-running workflows and their state |
| Orchestration | Controls the execution of activities |
| Transformation | Performs actual data processing |
| Activity Input JSON | Shows what ADF sent |
| Activity Output JSON | Shows what the external service returned |
| Execute Pipeline | Calls a child pipeline |
| Wait on completion | Controls whether the parent waits for the child |
| Idempotency | Prevents incorrect duplicate processing during reruns |

### 7. Important viva questions

**Q1. What is the difference between Stored Procedure Activity and Script Activity?**

Stored Procedure Activity executes an existing stored procedure, while Script Activity executes SQL scripts directly. Script Activity also supports Query and NonQuery execution and Output/InputOutput parameters.

**Q2. How do you pass parameters to a Databricks notebook?**

I create pipeline parameters, map them under Notebook Activity Base parameters, and retrieve them using `dbutils.widgets.get()` inside the notebook.

**Q3. How do you return output from Databricks to ADF?**

I use `dbutils.notebook.exit()` in the notebook and read the returned value using `@activity('RunNotebook').output.runOutput`.

**Q4. What is the difference between asynchronous execution and Durable Functions?**

Asynchronous execution is a way of running work without waiting for immediate completion. Durable Functions are an Azure Functions extension used to manage long-running workflows and their state.

**Q5. Why do we use Until Activity?**

Until Activity repeats a set of activities until a specified condition becomes true. It can be used to poll an external job until it completes.

**Q6. How do you debug parameters not arriving at an external service?**

I inspect Activity Input JSON, check dynamic expressions and parameter mapping, and verify that the receiving service reads the correct request field.

**Q7. What is the difference between orchestration and transformation?**

Orchestration controls what should happen and when. Transformation performs the actual data processing, such as joins, aggregations, and deduplication.

**Q8. Why should we chain pipelines safely?**

To control execution order, handle failures, pass parameters correctly, avoid duplicate processing, and make pipeline reruns reliable.

**Q9. What is idempotency?**

It means rerunning an operation should not produce duplicate or incorrect results.

**Q10. What is the difference between Activity Input and Output JSON?**

Input JSON shows what ADF sends to an activity. Output JSON shows the response or result returned by the activity.

---

### FINAL CONCEPT TO REMEMBER

ADF acts as the coordinator of the entire data workflow.

It can execute SQL scripts, call stored procedures, trigger notebooks, invoke external services, and chain pipelines.

But it should not be forced to perform every complex transformation itself. Instead, it should delegate processing to the appropriate engine, collect the result, handle failures, and continue the workflow safely.