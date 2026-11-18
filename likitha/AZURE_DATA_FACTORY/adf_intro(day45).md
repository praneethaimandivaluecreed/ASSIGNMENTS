ADF Studio and Your First Pipeline
Topic: Azure Data Factory – Beginner Data Engineering Notes
Page 1 – ADF Studio and Building Your First Pipeline
1. ADF Studio Tour
ADF Studio is the web-based interface where we create, manage, run and monitor Azure Data Factory pipelines.

It has three important sections:

1. Author
- Used to create and edit pipelines.
- Create linked services, datasets and activities.
- Configure pipeline parameters and variables.
- Debug and publish pipelines.
2. Monitor
- Used to track pipeline executions.
- Check successful, failed and in-progress runs.
- View activity execution details, input, output and error messages.
- Identify where and why a pipeline failed.
3. Manage
- Used to manage ADF resources and configurations.
- Create and manage linked services and Integration Runtimes.
- Configure triggers, Git settings and other factory-level settings.
2. Building Blocks of Your First Pipeline
To move data from a source to a destination, we generally use these four components:

1. Linked Service (Connection)
- Defines how ADF connects to an external service or data store.
- Contains connection information such as server name, database name and authentication details.
- Example: Connection to Azure Blob Storage or Azure SQL Database.
2. Dataset (Data Description)
- Represents the specific data we want to work with inside a data store.
- Defines the location and structure of the data.
- Example: A particular CSV file inside a storage container.
- A dataset uses a linked service to connect to its data store.
3. Pipeline (Workflow)
- A logical container that groups activities together.
- Defines the overall workflow of data movement or transformation.
- Example: A pipeline that copies customer data from Storage to SQL Database.
4. Activity (Actual Task)
- An individual task performed inside a pipeline.
- Examples: Copy Activity, Lookup Activity, Stored Procedure Activity and Web Activity.
- A pipeline can contain one or multiple activities.
Remember the relationship:
Pipeline
   |
   └── Activity (Copy Data)
           |
           ├── Source Dataset
           |       |
           |       └── Source Linked Service
           |
           └── Sink Dataset
                   |
                   └── Sink Linked Service


Simple example: Suppose we want to copy customers.csv from Azure Blob Storage to Azure SQL Database.
- Source Linked Service → Connects to Blob Storage.
- Source Dataset → Identifies customers.csv.
- Sink Linked Service → Connects to Azure SQL Database.
- Sink Dataset → Identifies the destination table.
- Copy Activity → Copies the data.
- Pipeline → Holds and executes the Copy Activity.
3. Test Connection
- Test Connection checks whether ADF can establish a connection to the configured data store.
- It helps identify incorrect connection details, authentication problems and connectivity issues.
- It is generally available while configuring a linked service.
Important: A successful Test Connection does NOT guarantee that the pipeline will run successfully. The activity may still fail because of incorrect file paths, missing tables, insufficient data permissions or other configuration issues.

Page 2 – Debugging, Monitoring and Run Types
4. Run with Debug
Debug is used to test a pipeline before publishing it.
- Open the pipeline in Author.
- Configure the activities and connections.
- Click Debug.
- ADF executes the pipeline using the current authoring configuration.
- Check whether the activities succeed or fail.
Important points:
- Debug helps test changes without publishing them first.
- Debug runs can be viewed in the Monitor section.
- Debug is mainly used during development and troubleshooting.
- Debug does not mean that a trigger has been started or scheduled.
5. Understanding Activity Input and Output JSON
When an activity executes, ADF records its Input and Output details.

Input JSON:
- Shows the configuration and values used by the activity during execution.
- Helps check source paths, sink details, parameters and evaluated expressions.
- Useful for identifying whether the activity received the correct input.
Output JSON:
- Shows the result produced by the activity.
- May contain rows copied, execution details, status, duration, output values or error information depending on the activity.
- Useful for checking whether the activity completed as expected.
Example:
Input:
{
  "source": "customers.csv",
  "destination": "customers"
}

Output:
{
  "rowsCopied": 500,
  "status": "Succeeded"
}


This is only an illustrative example; actual ADF JSON varies by activity.
6. Finding Failed Runs in Monitor
When a pipeline fails, use the Monitor hub to identify the problem.

Steps:
1. Open Monitor in ADF Studio.
2. Go to Pipeline runs.
3. Find the failed pipeline run.
4. Open the pipeline run to see its activities.
5. Identify the failed activity.
6. Open the activity details.
7. Check its Error message, Error code, Input and Output.
How to read an error:
- Error message: Explains what went wrong in simple or technical terms.
- Error code: Helps identify the category or specific cause of failure.
- Input: Helps check whether the activity received the correct values.
- Output: Helps understand the execution result and failure details.
7. First Questions to Ask When Debugging
Whenever a pipeline fails, don't randomly change settings. Follow this order:
Question	What to investigate
Which activity failed?	Identify the exact failed activity.
What was its input?	Check parameters, file paths and connection details.
What is the error code?	Understand the type of failure.
What does the error message say?	Identify the actual problem.
What should I fix?	Correct the connection, permissions, path or configuration.

Example: If Copy Activity fails with a file-not-found error:
- Which activity? Copy Activity.
- Input? Check the source file path.
- Error? File not found.
- Fix? Verify the container, folder and file name.
8. Pipeline Run vs Trigger Run vs Activity Run
These three terms are important for ADF interviews.
Run type	Meaning
Pipeline Run	One execution of the complete pipeline.
Activity Run	Execution of an individual activity inside a pipeline.
Trigger Run	An execution of a trigger that starts a pipeline based on a configured event or schedule.

Example:

Suppose a pipeline contains three activities:
Pipeline: SalesPipeline
       |
       ├── Lookup Activity
       ├── Copy Activity
       └── Stored Procedure Activity


- Pipeline Run → Represents the execution of SalesPipeline.
- Activity Run → Represents the individual execution of Lookup, Copy or Stored Procedure.
- Trigger Run → Represents a schedule or event trigger firing and starting the pipeline.
Important distinctions:
- One pipeline run can contain multiple activity runs.
- One trigger firing can start a pipeline run.
- A pipeline can also be started manually or through Debug without a trigger.
- A trigger run and pipeline run are not the same thing.
- An activity can fail even when the pipeline contains other successful activities.

Important Points to Remember ⭐
1. Author = Build pipelines; Monitor = Track executions; Manage = Configure and manage factory resources.
2. Linked Service = Connection; Dataset = Data location and structure.
3. Pipeline = Workflow; Activity = Individual task.
4. Test Connection checks connectivity, not the entire pipeline.
5. Debug is used to test pipeline changes before publishing.
6. Input JSON = What went into the activity; Output JSON = What came out.
7. Monitor helps identify failed pipeline runs and activity errors.
8. Always check failed activity → Input → Error code → Error message → Fix.
9. Pipeline Run = Complete pipeline execution; Activity Run = Individual task execution; Trigger Run = Trigger execution.