# Incremental Load Patterns – Azure Data Factory (ADF)

## 1. Full Load vs Incremental Load

### Full Load
Full load means copying the **entire source data to the destination every time the pipeline runs**, even if some records were already copied.

Example:
- Monday: 1,00,000 records → Copy 1,00,000.
- Tuesday: 1,05,000 records → Copy all 1,05,000 again.

**Advantages:**
- Easy to implement.
- No need to track previous loads.
- Useful for small tables and complete refreshes.

**Disadvantages:**
- Takes more time for large datasets.
- Uses more bandwidth and processing resources.
- Repeatedly copies unchanged data.

### Incremental Load
Incremental load means copying **only new or changed records since the previous successful load**.

Example:
- Monday: 1,00,000 records → Copy 1,00,000.
- Tuesday: 1,05,000 records → Copy only 5,000 new records.

**Advantages:**
- Faster for large datasets.
- Reduces unnecessary data movement.
- Saves processing time and cost.

**Disadvantages:**
- More complex to implement.
- Needs a mechanism to identify changes.
- Must handle duplicates, failures and late-arriving data.

**Important:** Incremental loading can capture inserts and updates, depending on the change-detection column. A simple watermark query cannot automatically detect deleted records.

---

## 2. High-Watermark Pattern

### What is a watermark?

A watermark is a value that tells the pipeline **up to which point data was successfully processed**.

Think of reading a book: Yesterday, you finished page 100. Today, you continue from page 101 instead of starting again.

Similarly, a data pipeline remembers its previous processing position.

A watermark can be:
- Timestamp (ModifiedDate).
- Increasing ID (OrderID).
- Sequence number.

### Watermark Table

A separate control table stores the last successfully processed watermark for each source table.

Example:

| TableName | LastWatermark |
|---|---|
| Orders | 2026-11-10 12:00 |
| Customers | 2026-11-09 15:30 |

Each table has its own watermark because different tables may be updated at different times.

Example SQL:

```sql
CREATE TABLE WatermarkTable
(
    TableName VARCHAR(100) PRIMARY KEY,
    LastWatermark DATETIME2
);
```

### Four steps in the High-Watermark Pattern

**Step 1: Lookup Old Watermark**

Use ADF **Lookup activity** to read the previous successful watermark.

```sql
SELECT LastWatermark
FROM WatermarkTable
WHERE TableName = 'Orders';
```

ADF expression:

```text
@activity('Lookup_Old_Watermark')
.output.firstRow.LastWatermark
```

**Step 2: Lookup New Watermark**

Find the latest eligible modification time in the source table.

```sql
SELECT MAX(ModifiedDate) AS NewWatermark
FROM Orders;
```

This gives the upper boundary for the current load.

ADF expression:

```text
@activity('Lookup_New_Watermark')
.output.firstRow.NewWatermark
```

**Step 3: Copy Delta**

Copy only records between the old and new watermark values.

```sql
SELECT *
FROM Orders
WHERE ModifiedDate > @OldWatermark
AND ModifiedDate <= @NewWatermark;
```

The logic is:

`OldWatermark < ModifiedDate <= NewWatermark`

- `>` avoids processing the previous boundary again.
- `<=` includes records at the new upper boundary.

**Step 4: Update Watermark**

After the Copy activity succeeds, use a Stored Procedure activity to update the watermark table.

```sql
UPDATE WatermarkTable
SET LastWatermark = @NewWatermark
WHERE TableName = 'Orders';
```

### Important rules

- Update the watermark **only after the destination load succeeds**.
- If Copy fails, keep the old watermark unchanged.
- If Copy succeeds but watermark update fails, the next run may copy the same range again. Therefore, the destination must be idempotent.
- If the source table is empty, `MAX()` returns NULL. Handle this safely instead of overwriting a valid watermark with NULL.
- If two records have the same timestamp, a timestamp-only watermark can miss records that arrive later with that same timestamp. Use a composite watermark, overlap window or change-tracking mechanism.
- An increasing ID is suitable for append-only data, but it cannot detect updates to existing records.
- A reliable ModifiedDate column is preferable for detecting inserts and updates.

---

## 3. Make Loads Safe to Rerun (Idempotency)

### What is Idempotency?

Idempotency means **running the same operation multiple times should produce the same final result as running it once**.

Example:

A pipeline copies 10,000 records successfully but fails before updating the watermark.

When rerun, it copies the same 10,000 records again.

If we simply append the records, duplicates will be created.

### Why is it important?

ADF pipelines can fail due to:
- Network issues.
- Database timeouts.
- Integration Runtime failures.
- Destination storage problems.
- Manual cancellation.

A pipeline should be safe to rerun without creating duplicates or corrupting data.

### Methods to achieve Idempotency

**1. UPSERT / MERGE (SQL destination)**

- If the record already exists → UPDATE it.
- If the record is new → INSERT it.

```sql
MERGE INTO TargetOrders AS T
USING StagingOrders AS S
ON T.OrderID = S.OrderID

WHEN MATCHED THEN
    UPDATE SET T.Amount = S.Amount

WHEN NOT MATCHED THEN
    INSERT (OrderID, Amount)
    VALUES (S.OrderID, S.Amount);
```

**2. Delete and Reload (File-based destination)**

For example, if loading the November 10 partition:

`orders/year=2026/month=11/day=10/`

Instead of appending the same files during every rerun:
- Replace the affected partition.
- Reload the complete batch.
- Mark it complete after validation.

**3. Deduplication**

Use a unique business key, such as OrderID, and keep the latest reliable version.

```sql
ROW_NUMBER() OVER
(
    PARTITION BY OrderID
    ORDER BY ModifiedDate DESC
)
```

Keep only rows where `ROW_NUMBER() = 1`.

**Remember:**
- Watermark tells us WHAT to load next.
- Idempotency ensures that loading it again does not create incorrect results.

### Correct production sequence

1. Read old watermark.
2. Get new watermark.
3. Copy delta into staging.
4. Validate the data.
5. MERGE into the destination or replace the partition.
6. Update the watermark only after successful destination loading.

Destination loading and watermark updating may happen in separate systems, so they cannot always be committed in one transaction. Design both operations to handle retries safely.

---

## 4. Late-Arriving Data and Overlap Windows

### What is Late-Arriving Data?

Late-arriving data means a record becomes available in the source later than its actual business event time.

Example:

An order was placed on November 10 but reached the source database only on November 12.

| OrderID | OrderDate | Created in Source |
|---|---|---|
| 101 | Nov 10 | Nov 10 |
| 102 | Nov 10 | Nov 10 |
| 103 | Nov 10 | Nov 12 |

If the pipeline uses OrderDate as its watermark, order 103 may be missed because its OrderDate belongs to an already processed period.

### Event Time vs Processing Time

- **OrderDate / EventTime:** When the actual business event happened.
- **CreatedAt:** When the record was created in the source database.
- **ModifiedDate:** When the record was last updated.
- **IngestedAt:** When the record entered the ingestion system.

For incremental extraction, use a reliable change or ingestion timestamp whenever possible, rather than blindly using the business event date.

### What is an Overlap Window?

An overlap window means reprocessing a small portion of previously processed data to capture late-arriving records or changes.

Example:

- Old watermark = November 11.
- Overlap duration = 2 days.
- Instead of starting from November 11, start from November 9.

```sql
SELECT *
FROM Orders
WHERE ModifiedDate >= DATEADD(
    DAY, -2, @OldWatermark
)
AND ModifiedDate <= @NewWatermark;
```

This captures data from the previous two days as well as new data.

### Why do we need Idempotency with Overlap?

Overlap deliberately reads some records again.

If we append them blindly, duplicates will appear.

Therefore:

**Overlap Window + Deduplication / MERGE = Safer Incremental Load**

### Important points

- Overlap duration depends on how late the source data usually arrives.
- A 2-day overlap cannot capture a record that arrives months late.
- Use periodic full reconciliation or a separate backfill process for very late data.
- A ModifiedDate column must be reliably updated whenever a record changes.
- Overlap is a safety mechanism, not a guarantee that every late record will be captured.

---

## 5. Change Tracking and CDC (Concept Only)

A normal watermark query has limitations, especially when records are deleted.

Example:

- INSERT: New record is added.
- UPDATE: Existing record is modified.
- DELETE: Existing record is removed.

A watermark can detect inserts and updates if the watermark column is reliable, but it cannot directly detect a deleted row because that row no longer exists in the source table.

### Change Tracking

Change Tracking is a SQL Server feature that identifies which rows have changed.

It tells us:
- Which primary key changed.
- Whether the operation was INSERT, UPDATE or DELETE.
- The associated change version.

It does not store a complete history of old and new column values.

Think of it as knowing which pages of a book were edited, without keeping every previous version.

### CDC (Change Data Capture)

CDC captures detailed changes made to database tables and stores them in special change tables.

It captures:
- INSERT operations.
- UPDATE operations.
- DELETE operations.

It can preserve historical change information, including changed column values.

Think of CDC as keeping a record of what changed on a page, rather than just knowing which page was edited.

### Change Tracking vs CDC

| Feature | Change Tracking | CDC |
|---|---|---|
| Identifies changed rows | Yes | Yes |
| Detects deletes | Yes | Yes |
| Detailed historical changes | No | Yes |
| Before/after values | No | Available |
| Storage/processing overhead | Generally lighter | Generally higher |

**When to use:**
- Change Tracking: When you only need to know which rows changed and retrieve their latest values.
- CDC: When you need detailed change information and historical values.

Both require proper source configuration and retention management. If the saved tracking version or LSN has expired, you may need a new full load or reconciliation.

---

## 6. Debugging Incremental Loads in ADF

| Problem | Possible reason | What to check / solution |
|---|---|---|
| Duplicate records | Pipeline rerun or overlap with append | Check watermark and use MERGE, deduplication or partition replacement |
| Missing rows | Wrong watermark column, late data or incorrect query boundaries | Check old/new values, timestamp precision and source data |
| Watermark not advancing | Copy failed or Stored Procedure failed | Check activity status, dependency conditions and SQL update |
| Watermark updated too early | Update activity ran before Copy completed | Connect watermark update using the Copy activity's Success dependency |
| Wrong time zone | Source and pipeline timestamps use different time zones | Check UTC vs local time and use consistent timestamp handling |
| Data type error | String, datetime and integer values are mixed | Check parameter types and convert values correctly |
| NULL watermark | Empty source or MAX() returned NULL | Handle NULL safely and do not overwrite a valid watermark |
| Same timestamp records missed | Timestamp-only watermark is not unique | Use composite watermark or overlap with deduplication |
| Pipeline becomes slow | Full table scan or inefficient source query | Check query plan, watermark column indexing, throughput and Integration Runtime |
| Simultaneous pipeline runs | Two runs read the same old watermark | Prevent overlapping runs or use concurrency control |

### Important Debugging Practices

1. Open ADF Monitor and check the failed activity.
2. Inspect activity Input and Output to verify the actual evaluated watermark values.
3. Check whether Copy is filtering the correct date/ID range.
4. Compare source and destination record counts.
5. Check whether the watermark update happened only after successful loading.
6. Check the time zone, timestamp format and data types.
7. Rerun safely without creating duplicates.

**Important:** A pipeline showing Succeeded does not always mean all expected business records were loaded. Always validate data completeness.

---

## Quick Revision – Interview Points

| Concept | One-line meaning |
|---|---|
| Full Load | Copies the entire dataset |
| Incremental Load | Copies only new or changed data |
| Watermark | Remembers the last processed boundary |
| Old Watermark | Previous successful position |
| New Watermark | Current extraction upper boundary |
| Lookup | Reads watermark values |
| Copy | Transfers delta records |
| Stored Procedure | Updates watermark |
| Idempotency | Makes reruns safe |
| MERGE | Updates existing and inserts new records |
| Late-arriving data | Data arrives later than expected |
| Overlap Window | Reprocesses a previous time range |
| Change Tracking | Identifies changed rows |
| CDC | Captures detailed change information |

### Interview Answering Strategy

Whenever an interviewer gives you an incremental loading failure scenario, think in this order:

1. **Identify the problem:** What failed and why?
2. **Protect data correctness:** Avoid missing records and duplicates.
3. **Recover safely:** Rerun using the correct watermark range and an idempotent destination operation.

**Final principle to remember:**

A good incremental pipeline should be efficient, should not miss data, should not create duplicates, and should be safe to rerun after failures.