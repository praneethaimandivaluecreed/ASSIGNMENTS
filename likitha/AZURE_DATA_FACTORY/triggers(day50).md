# Azure Data Factory — Running Notes
## Topic: Triggers and Scheduling

*Beginner Data Engineering Notes | Simple explanations + practical examples + debugging*

---

## 1. What is a trigger in Azure Data Factory?

A **trigger** is a mechanism that tells Azure Data Factory (ADF) when to start a pipeline.

A pipeline contains the work (Copy, Lookup, Data Flow, etc.). A trigger decides **when that work should begin**.

Think of it this way:

- **Pipeline** = the work to be done.
- **Trigger** = the alarm that tells the pipeline when to start.

ADF has four important trigger types:

| Trigger | When does it run? | Common use |
|---|---|---|
| Schedule | At configured dates/times or intervals | Daily reports |
| Tumbling window | For fixed, continuous time windows | Hourly data processing and backfills |
| Storage event | When a matching storage event happens | Process a file after upload |
| Custom event | When a matching custom Event Grid event happens | Start processing after an application publishes an event |

### How triggers and pipelines are related

- **Schedule and event triggers:** A trigger can be associated with multiple pipelines, and a pipeline can be associated with multiple schedule/event triggers.
- **Tumbling window trigger:** It has a one-to-one relationship with its pipeline. One tumbling window trigger is associated with one pipeline.

This distinction matters when designing reusable pipelines and when investigating unexpected multiple runs.

---

## 2. Create the different types of triggers

### A. Schedule trigger

A schedule trigger starts a pipeline at a particular time or according to a recurring calendar.

**Example:** Run a sales pipeline every day at 9:00 AM.

Important settings:

- **Start time:** When the trigger becomes eligible to start its schedule.
- **End time:** When the trigger should stop firing.
- **Time zone:** The time zone used to interpret the schedule.
- **Recurrence:** How often it should run.
- **Calendar rules:** Specific days, dates or occurrences on which it should run.
- **Runtime state:** Whether the trigger is started, stopped or otherwise inactive. This is a status, not a field you directly edit to activate it; use the Start/Stop operation.

ADF schedule triggers support calendar rules such as:
- `weekDays`: Run on selected weekdays.
- `monthDays`: Run on selected dates from 1 to 31. Negative values can count backward from month-end; `-1` means the last day of the month.
- `monthlyOccurrences`: Select relative dates, such as the first Sunday or last Friday of a month.

**Important scheduling examples and pitfalls**

1. If the start time is in the past, a schedule trigger does not automatically backfill every missed run. It calculates the next eligible future occurrence.
2. If the start time is in the future, the trigger waits until that time and then follows its recurrence rules.
3. The start time and calendar rule must make sense together. For example, a start time on Tuesday with a Friday-only rule will not produce a Tuesday run.
4. A monthly rule such as `monthDays: [31]` will not run in months that do not have a 31st day. For month-end processing, consider the supported last-day rule instead.
5. Always check the time zone. A schedule configured for 9:00 AM UTC is 2:30 PM in India (IST).

**When to use it:** When the pipeline must run at a regular clock time and you do not need ADF to maintain individual historical time-window state.

### B. Tumbling window trigger

A tumbling window trigger divides time into **fixed-size, continuous, non-overlapping windows**.

Example: An hourly trigger creates windows like:

- 10:00–11:00
- 11:00–12:00
- 12:00–13:00

Unlike a normal schedule trigger, a tumbling window trigger keeps track of each window's execution state. It is useful when every time period matters and missed historical periods must be processed.

**Important properties**

| Property | Meaning |
|---|---|
| Frequency | Base unit: minute, hour or other supported unit |
| Interval | Number of frequency units in one window |
| Start time | Beginning of the window sequence |
| End time | Optional point at which the sequence stops |
| Delay | Extra waiting time after a window ends, allowing late-arriving data to settle |
| Max concurrency | Maximum number of windows allowed to run at the same time |
| Retry policy | Controls automatic retry attempts after pipeline failure |
| Runtime state | Indicates whether the trigger is active or stopped |

**Frequency and interval example**

If frequency = `Hour` and interval = `3`, each window covers three hours:

- 01:00–04:00
- 04:00–07:00
- 07:00–10:00

If frequency = `Hour` and interval = `1`, each window covers one hour.

**Delay example**

Suppose the 1:00–2:00 PM window ends at 2:00 PM and delay is 10 minutes. ADF waits an additional 10 minutes before starting the pipeline for that window. This gives late-arriving data some time to arrive.

Delay changes when processing begins; it does not change the actual window boundaries.

**Max concurrency**

Tumbling window triggers have an explicit `maxConcurrency` setting, up to 50 concurrent runs.

For example, suppose 24 historical hourly windows need backfilling and `maxConcurrency = 10`. ADF can process up to 10 eligible windows at once, then use the available slots for the remaining windows as earlier runs finish.

- **Concurrency** controls how many windows can run together.
- **Dependencies** can enforce an order between windows.
- Without a dependency requiring sequential execution, do not assume that all windows must run one after another.

If a pipeline regularly takes longer than its window size, windows may remain in `Waiting` status and a backlog can form. Investigate compute capacity, query performance, partitioning and window size.

**Important:** Frequency and interval cannot be changed after the tumbling window trigger is created. This restriction protects window reruns and dependency calculations. Plan these values carefully.

### C. Storage event trigger

A storage event trigger starts a pipeline when a matching event happens in Azure Blob Storage or supported storage.

**Example:** Start a pipeline whenever a `.csv` file is uploaded into the `incoming` folder.

The flow is:

1. A user or application uploads a file.
2. Storage generates an event, such as `BlobCreated`.
3. Azure Event Grid receives the event.
4. Event Grid checks the event subscription and its path filters.
5. If the event matches, it sends the event to the ADF trigger.
6. ADF checks its trigger settings and starts the pipeline.
7. The file details can be passed into pipeline parameters.

**Path filters**

For example:

- Begins with: `/data/blobs/incoming/`
- Ends with: `.csv`

The special `/blobs/` segment is part of the ADF storage-event path format.

Examples of file filters:

- `*.csv` — CSV files, depending on the configured filter pattern.
- `sales_*.csv` — matching sales-prefixed CSV files.

**Important setting: `ignoreEmptyBlobs`**

Its default is `true`. Therefore, zero-byte files are ignored by default. If the business requirement is to trigger even for empty files, review this setting.

Even if an empty file triggers the pipeline, the pipeline should still validate whether the file is usable.

### D. Custom event trigger

A custom event trigger starts a pipeline when an application or service publishes a custom event to Azure Event Grid.

Example:

1. An application finishes generating a customer report.
2. It publishes a custom event such as `ReportReady`.
3. Event Grid routes the event to the configured subscription.
4. The ADF custom event trigger receives the matching event.
5. The pipeline starts and can use event details as parameters.

Use a custom event trigger when the event represents a business action or application event, rather than simply a file being created in storage.

---

## 3. Schedule vs. tumbling window: backfill, retries and dependencies

This is one of the most important differences to understand.

| Feature | Schedule trigger | Tumbling window trigger |
|---|---|---|
| Main idea | Fire at a configured time | Process fixed time windows |
| Remembers each window's state | No tumbling-window state | Yes |
| Historical backfill | Does not automatically replay missed schedule times | Supports historical windows/backfill |
| Retries | Configure pipeline activity retry where appropriate; schedule trigger itself does not provide tumbling-window retry behavior | Trigger retry policy can retry the pipeline for the same window |
| Dependencies between windows | No tumbling-window dependency mechanism | Supports window dependencies and self-dependencies |
| Concurrency | No tumbling-window `maxConcurrency` property | Has `maxConcurrency`, up to 50 |
| Run status | Usually represents whether the trigger successfully started the pipeline | Reflects the associated pipeline's result for that window |

### What is backfilling?

Backfilling means processing historical time periods that have not yet been processed.

Example: An hourly pipeline was unavailable for five hours.

With a schedule trigger, the missed times are not automatically replayed as historical windows.

With a tumbling window trigger, you can configure a historical start time and process the corresponding windows. For example, a start time 24 hours in the past with hourly windows creates 24 historical windows to process.

**Backfill does not necessarily run at real-time speed.** If concurrency slots are available, historical windows can run faster than the clock. Once ADF catches up to the present, it waits for future windows to become due.

### What happens when a tumbling window pipeline fails?

A tumbling window trigger can retry the pipeline automatically using the same window input parameters.

The retry policy includes:

- `count`: Number of retry attempts. Default is `0`, meaning no configured retries.
- `intervalInSeconds`: Delay between retry attempts. Default is 30 seconds; minimum is 30 seconds.

Retries help with temporary failures, such as a short-lived service interruption. They do not fix permanent problems such as invalid SQL, wrong paths or bad data. Fix the root cause before manually rerunning a failed window.

### Tumbling window dependencies

Dependencies allow one tumbling window trigger to wait for another trigger's corresponding window to finish successfully.

Example:

- Trigger A loads raw sales data.
- Trigger B transforms the raw sales data.
- Trigger B should run only after Trigger A's matching window succeeds.

A **self-dependency** means a window waits for an earlier window of the same trigger.

Important dependency properties:

- `type`: The dependency reference type.
- `size`: The size of the dependency window. If omitted, it defaults to the child trigger's window size.
- `offset`: The time offset used to identify the dependency window. For self-dependency, the offset must be negative. If omitted for a non-self dependency, the matching window is used.

**Example:** If the 11:00–12:00 window must wait for the previous 10:00–11:00 window, the dependency points to the earlier window.

A downstream dependency can wait up to seven days for its upstream dependency. If the dependency is not satisfied within that period, the dependent window can fail.

A window that is `Waiting on dependency` has not started its pipeline yet. In the documented behavior discussed, it cannot be manually canceled while it is still waiting on the dependency; resolve the dependency first.

**Dependency warning:** Incorrect self-dependency offsets can cause windows to remain stuck in `Waiting on dependency`. Always verify that the dependency points to a valid earlier window.

### Slow pipelines and backlog

Suppose the 1:00–2:00 window takes 90 minutes to finish. The next hourly window may have to wait for an available slot or dependency. Later windows can also build up behind it.

This is called a backlog or backpressure.

Possible fixes:
- Increase available compute resources.
- Optimize SQL queries and transformations.
- Review partitioning and data volume.
- Reconsider whether the window size is too small for the workload.
- Review `maxConcurrency` and dependency settings.

Do not simply increase concurrency without considering the load on the source database or API.

---

## 4. Pass trigger values into pipeline parameters

A trigger can pass information to a pipeline when it starts.

The basic flow is:

**Trigger → Pipeline parameters → Activities**

A pipeline parameter is an input received when the pipeline run starts. Activities can then use that parameter through dynamic content.

### A. Tumbling window values

ADF provides the tumbling window values:

```text
@trigger().outputs.windowStartTime
@trigger().outputs.windowEndTime
```

These expressions represent the start and end of the particular window that started the pipeline.

Example:

- Window start: 11:00 AM
- Window end: 12:00 PM

Pass these values into pipeline parameters such as `pWindowStart` and `pWindowEnd`.

Then use them in a SQL query:

```sql
SELECT *
FROM Sales
WHERE TransactionDate >= '@{pipeline().parameters.pWindowStart}'
  AND TransactionDate <  '@{pipeline().parameters.pWindowEnd}';
```

The important idea is to use a **half-open interval**:

- Include records where timestamp is greater than or equal to the start.
- Exclude records where timestamp is greater than or equal to the end.

This avoids counting a boundary record in two adjacent windows.

### B. Storage event values

For a storage event trigger, useful event values include:

```text
@triggerBody().folderPath
@triggerBody().fileName
```

These provide the folder path and file name from the event.

Pass them into pipeline parameters, for example:

- `pFolderPath`
- `pFileName`

The Copy activity can use these parameters to construct a dynamic source path.

Conceptually:

```text
container + folderPath + fileName
```

This lets one pipeline process many files without hardcoding a different file name for every run.

### C. Important difference: time filtering vs. timestamp-based output folders

Suppose an API returns the entire current dataset but does not support filtering by date.

You can still use tumbling window parameters to create time-organized output folders, such as:

```text
/year=2026/month=11/day=06/hour=13/data.parquet
```

But be careful: **naming a file with a window timestamp does not mean the API returned only records from that time window.**

- If the source has a timestamp column and you filter using the window boundaries, you can extract records for that actual time slot.
- If the API returns a complete snapshot without a usable timestamp filter, you are capturing a snapshot and organizing it under a window-based path.

This distinction is important when designing historical backfills.

---

## 5. Publish, then start the trigger: why it may not fire

Creating a trigger does not automatically mean that it is active in the live Data Factory.

Think of a trigger as an alarm clock:

| ADF operation | Alarm clock analogy |
|---|---|
| Create | Set the alarm |
| Save | Save the alarm settings |
| Publish | Make the settings available to the live system |
| Start | Switch the alarm ON |
| Trigger fires | The alarm rings |

**Important differences:**

- **Save:** Saves your authoring changes.
- **Commit:** Commits changes to the Git repository when using Git integration.
- **Publish:** Deploys your collaboration-branch changes to the live Data Factory.
- **Start:** Activates the trigger.

A published trigger can exist in the live Data Factory but still be inactive. It will not fire until it is started, or otherwise activated through the supported deployment/activation workflow.

The activation checkbox and the separate Start operation are two ways of controlling the trigger's activation lifecycle. Therefore, do not assume that every trigger always needs a separate manual Start after publishing; check its actual runtime state.

**Practical sequence:**

1. Create or modify the trigger.
2. Save your changes.
3. Publish the changes.
4. Check the trigger's runtime state.
5. Start it if it is not active.
6. Wait for the next eligible schedule time or matching event.
7. Check Monitor → Trigger runs.

---

## 6. Debugging: trigger did not run or duplicate runs happened

When a pipeline has not executed, do not immediately assume that the pipeline itself is broken.

### First debugging rule

**Always inspect Trigger runs first.**

- If no trigger run exists, investigate trigger activation, schedule, time zone, event configuration or deployment.
- If a trigger run exists but no expected successful pipeline run exists, inspect the trigger run details and associated pipeline run.
- If the pipeline run exists but failed, inspect the pipeline's activity runs.

### A. Schedule trigger did not run

Check these in order:

1. **Published?** Were the latest trigger changes published?
2. **Started?** Is the trigger's runtime state active?
3. **Start date/time?** Has the start time been reached?
4. **End date/time?** Has the trigger already passed its end time?
5. **Recurrence?** Does the configured calendar rule actually include the expected day and time?
6. **Time zone?** Are you interpreting the schedule in the correct time zone?
7. **Runtime state?** Is the trigger stopped or inactive?

Remember: a schedule trigger does not automatically replay missed historical times just because its start time was in the past.

### B. Storage event trigger did not run

Understand the event flow:

**Storage upload → Event Grid → Event subscription filters → ADF event trigger → Pipeline run**

Check:

- Is the file uploaded to the correct storage account and container?
- Is the event subscription configured?
- Does the file path match the **Begins With** filter?
- Does the file name match the **Ends With** filter?
- Is the expected event type selected, such as `BlobCreated`?
- Is the special `/blobs/` segment included in the path format?
- Is `ignoreEmptyBlobs` filtering out a zero-byte file?
- Was the file upload completed and committed?
- Is the trigger published and started?

A file in the wrong folder or with the wrong extension will not match the configured filters.

### C. Why did the pipeline run more than once?

Common causes:

1. **Multiple triggers:** More than one trigger is associated with the same pipeline.
2. **Event Grid redelivery:** Event Grid uses at-least-once delivery. The same event may be delivered more than once, for example after a temporary delivery or acknowledgement problem.
3. **Overlapping event filters/subscriptions:** More than one event subscription or trigger may match the same file.
4. **File creation/overwrite behavior:** Uploading or replacing a file can generate another storage event.
5. **Stopping and restarting an event trigger:** Review trigger history and event-subscription behavior if unexpected executions appear after a restart.

**Important engineering lesson: design event-based pipelines to tolerate duplicate events.**

This is called making processing **idempotent**: processing the same event again should not create duplicate business data.

Examples:
- Track processed files using a unique file path or event identifier.
- Use a unique business key in the destination table.
- Use SQL `MERGE` or an equivalent upsert strategy.
- Use a staging table and controlled final load.
- Use a unique constraint or atomic claim when multiple runs may try to process the same file.

Do not confuse two things:
- **Duplicate pipeline runs:** The pipeline was started more than once.
- **Duplicate data:** The destination contains repeated records.

A duplicate run does not always mean duplicate data if the pipeline is designed safely.

---

## 7. Rerun a failed tumbling window and read Trigger runs

A tumbling window trigger maintains state for each individual time window. If one window fails, you can rerun that particular window after fixing the problem.

### Example

Suppose these hourly windows ran:

| Window | Status |
|---|---|
| 09:00–10:00 | Succeeded |
| 10:00–11:00 | Succeeded |
| 11:00–12:00 | Failed |
| 12:00–13:00 | Waiting on dependency |

The 11:00–12:00 window failed because the destination database was temporarily unavailable.

Correct approach:

1. Open **Monitor → Trigger runs**.
2. Find the failed tumbling window.
3. Inspect its trigger run details.
4. Open the associated pipeline run.
5. Inspect the failed activity's input, output and error message.
6. Fix the root cause (for example, correct the database connection).
7. Publish the corrected pipeline if its definition changed.
8. Rerun the specific failed tumbling window.
9. Verify that the window succeeds.
10. Check whether dependent windows can now proceed.

**Why rerun the window instead of simply running the pipeline again?**

A normal pipeline rerun is not necessarily the same as rerunning the original tumbling window. The window rerun preserves the original window's time boundaries and trigger context, which is important for correct historical processing and dependencies.

### What does the Trigger runs view show?

Go to **Monitor → Trigger runs**.

Use it to inspect:
- Trigger name and trigger run ID.
- Start and end times.
- Window start and end times for tumbling windows.
- Status.
- Error information and associated pipeline run details.

Exact columns and actions can vary with the ADF Studio interface.

### Tumbling window statuses

| Status | Meaning |
|---|---|
| Running | Pipeline is executing for that window |
| Waiting | Window is eligible but waiting for an available concurrency slot |
| Waiting on dependency | Waiting for an upstream or self-dependency to succeed |
| Succeeded | Pipeline completed successfully for that window |
| Failed | Pipeline failed after configured retry attempts |
| Canceled | Run was canceled |

### Schedule and event trigger statuses

- **Succeeded:** Trigger successfully fired and started the pipeline.
- **Failed:** Trigger could not fire or start the pipeline successfully.
- **Canceled:** Run was canceled.

Schedule and event triggers do not have the tumbling-window `Waiting` and `Waiting on dependency` states.

**Very important difference:** A schedule trigger generally follows a fire-and-forget model. Its trigger run can show success once it has successfully started the pipeline, even if the pipeline later fails. A tumbling window trigger's state reflects the associated pipeline result for that window.

### Extra tumbling window points to remember

- A dependency wait can last up to seven days before the dependent window fails.
- `maxConcurrency` controls how many windows can execute concurrently.
- `delay` adds a buffer after a window ends; it does not change the window boundaries.
- Frequency and interval cannot be changed after trigger creation.
- Changing the end time does not reset already processed windows. A new end time is honored for future window processing.
- If a trigger has a long historical backlog, check its start time and concurrency before starting it. An accidental start time years in the past can create a very large backfill and overload a source system.
- If windows are waiting for too long, investigate concurrency, dependencies and pipeline duration rather than assuming the trigger is broken.

---

## 8. Quick revision: the complete debugging checklist

When a trigger does not behave as expected, follow this order:

1. **Trigger runs:** Is there a trigger run at all?
2. **Publish:** Are the latest changes deployed?
3. **Runtime state:** Is the trigger active?
4. **Schedule:** Check start time, end time, recurrence and time zone.
5. **Storage event:** Check event type, storage path, file extension, Event Grid subscription and empty-file setting.
6. **Tumbling window:** Check window boundaries, delay, concurrency and dependencies.
7. **Pipeline run:** If it started, inspect the associated pipeline run.
8. **Activity runs:** Find the exact failed activity and inspect its input/output/error.
9. **Rerun:** Fix the cause and rerun the correct failed tumbling window.
10. **Duplicate protection:** Make the destination load idempotent.

### Interview-ready questions

**1. What is the main difference between schedule and tumbling window triggers?**  
A schedule trigger starts a pipeline at configured times. A tumbling window trigger processes fixed time windows and maintains state for each window, which supports backfills, retries and dependencies.

**2. Why did my trigger not run after I created it?**  
It may not have been published or activated. I would check Publish status, runtime state, start time, recurrence and time zone.

**3. What is the purpose of `maxConcurrency`?**  
It controls how many tumbling windows can run at the same time, up to 50.

**4. Does a timestamp-based output folder mean I extracted only that time period's records?**  
No. The folder name only organizes the output. To extract actual time-slot records, the source must support filtering using the window boundaries or equivalent logic.

**5. Why can an event trigger cause duplicate runs?**  
Multiple triggers or subscriptions may match the same event, and Event Grid can redeliver events. I would make the pipeline idempotent.

**6. What should I inspect first when a pipeline has not executed?**  
Trigger runs. If there is no trigger run, investigate trigger activation, scheduling, event configuration and publishing. If there is a pipeline run, inspect its activities.

**7. Why rerun a failed tumbling window instead of starting a new pipeline run?**  
Rerunning the window preserves its original time boundaries and trigger context, which matters for historical correctness and dependencies.

---

## 9. References

1. [Azure Data Factory Triggers — overview (Medium)](https://medium.com/@hasninemirza/azure-data-factory-triggers-cdb193142c9e)
2. [Create a tumbling window trigger](https://learn.microsoft.com/en-us/azure/data-factory/how-to-create-tumbling-window-trigger?tabs=data-factory%2Cazure-powershell)
3. [Create tumbling window trigger dependencies](https://learn.microsoft.com/en-us/azure/data-factory/tumbling-window-trigger-dependency)
4. [Pipeline execution and trigger types](https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipeline-execution-triggers#trigger-types)
5. [Trigger parameterization — pass trigger information to a pipeline](https://learn.microsoft.com/en-us/azure/data-factory/how-to-use-trigger-parameterization)
6. [Visually monitor Azure Data Factory](https://learn.microsoft.com/en-us/azure/data-factory/monitor-visually)
7.[chatgpt](https://chatgpt.com/share/6aeda550-71a0-83ee-bf7e-87e88b97521b)

*Revision reminder: A trigger decides when a pipeline starts. A pipeline performs the work. Monitor the trigger first, then the pipeline, then the individual activity. For tumbling windows, always keep the original window boundaries and dependency state in mind when rerunning.*