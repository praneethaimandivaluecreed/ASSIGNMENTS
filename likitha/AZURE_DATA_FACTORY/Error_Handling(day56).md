# Azure Data Factory – Error Handling, Logging and Alerts

## 1. Retries and Timeouts

- **Retry:** Number of additional attempts ADF makes when an activity fails.
- **Retry interval:** Waiting time between retry attempts.
- **Timeout:** Maximum time an activity is allowed to run.

**Example:** Retry = 3 means 1 original attempt + 3 retries = 4 maximum attempts.

**Remember:**
- Retries help with temporary failures like network issues.
- They won't fix permanent errors like wrong credentials or incorrect file paths.
- Increasing timeout does not fix an activity that is stuck or incorrectly configured.

## 2. Failure Paths and Try-Catch Pattern

ADF does not have a separate Try-Catch activity. We create a similar pattern using **Dependency Conditions**.

Four dependency conditions:
- **Upon Success:** Runs when the previous activity succeeds.
- **Upon Failure:** Runs when the previous activity fails.
- **Upon Completion:** Runs whether the previous activity succeeds or fails.
- **Upon Skip:** Runs when the previous activity is skipped.

**Example:** Copy Data → Upon Failure → Log Error → Send Email → Fail Activity.

- The failure branch can log errors or send notifications.
- **Fail activity** intentionally marks the pipeline as Failed. It has Error Code and Error Message fields.
- Logging an error or sending an email alone does not guarantee that the pipeline will be marked as Failed.

## 3. Custom Run Log Table

We can create a SQL table named `PipelineRunLog` to maintain pipeline execution details.

| Column | Purpose |
|---|---|
| RunId | Unique pipeline execution ID |
| PipelineName | Pipeline name |
| StartTime | Pipeline start time |
| EndTime | Pipeline end time |
| RowsCopied | Number of rows copied |
| Status | Running / Succeeded / Failed |
| ErrorMessage | Failure details |

**Logging process:**
1. Before execution, insert a record with Status = Running and StartTime.
2. After success, update Status = Succeeded, EndTime and RowsCopied.
3. After failure, update Status = Failed, EndTime and ErrorMessage.

**Useful ADF expressions:**
- Run ID: `@pipeline().RunId`
- Pipeline name: `@pipeline().Pipeline`
- Current time: `@utcNow()`
- Rows copied: `@activity('CopyCustomerData').output.rowsCopied`
- Error message: `@activity('CopyCustomerData').error.message`

**Remember:** `rowsRead` = rows read, `rowsCopied` = rows copied, and `rowsSkipped` = rows skipped. Copy activity output may not be available on the failure path, so handle missing values safely.

## 4. Monitor Hub and Rerun

ADF Monitor Hub helps us track pipeline and activity executions.

- **Pipeline Runs:** Shows the overall pipeline execution status, Run ID and execution time.
- **Activity Runs:** Shows the status and details of individual activities.

**Debugging steps:**
1. Open Monitor → Pipeline Runs.
2. Filter by pipeline name, status or time range.
3. Open the failed pipeline run.
4. Check Activity Runs and select the failed activity.
5. Inspect Input, Output and Error details to identify the problem.

**Rerun from failed activity:** Starts a new pipeline execution from the selected failed activity instead of starting from the beginning. It does not guarantee resuming from the exact row or byte where execution stopped.

**Important:** Design pipelines to be **idempotent**, meaning rerunning them should not create incorrect duplicate data. Use MERGE/UPSERT, unique keys or suitable overwrite strategies.

## 5. Failure Alerts and Email Notifications

**Azure Monitor Alert Rule:**
- An Alert Rule checks whether a failure condition has occurred.
- Example: Trigger an alert when failed pipeline runs are greater than zero.
- An **Action Group** defines what happens after the alert is triggered, such as sending an email or SMS.

**Remember:**
- Alert Rule = When to trigger an alert.
- Action Group = What action to perform.

**Custom email using Logic Apps:**

ADF Web Activity → Azure Logic App → Outlook Email.

The Web Activity calls an HTTP-triggered Logic App and passes details such as pipeline name, Run ID, failed activity and error message. Logic Apps then sends a customized email.

## 6. Pipeline Succeeded Even Though an Activity Failed

**Problem:** Copy Data fails, but the failure branch sends an email successfully. The overall pipeline may still show Succeeded because the error-handling activity succeeded.

**Solution:** Add a **Fail activity** after logging the error and sending the notification.

Example:

`Copy Data → Upon Failure → Log Error → Send Email → Fail Activity`

This ensures the overall pipeline is marked as Failed.

**Key takeaway:** A good error-handling design should retry temporary failures, log errors, send notifications, preserve the correct pipeline status and support safe reruns.