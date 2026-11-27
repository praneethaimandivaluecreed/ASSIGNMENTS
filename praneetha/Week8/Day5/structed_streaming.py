
import json
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField, StringType, TimestampType, DoubleType
)
from pyspark.sql.functions import col, window, sum as spark_sum


spark = (
    SparkSession.builder
    .appName("BasicFileSourceStreaming")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")


BASE_DIR = Path("streaming_demo")
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "parquet_output"
CHECKPOINT_DIR = BASE_DIR / "checkpoint"

INPUT_DIR.mkdir(parents=True, exist_ok=True)


sample_data = {
    "batch1.json": [
        {
            "event_id": "E1",
            "customer_id": "C1",
            "event_time": "2026-01-01T10:00:00",
            "amount": 100.0
        },
        {
            "event_id": "E2",
            "customer_id": "C1",
            "event_time": "2026-01-01T10:02:00",
            "amount": 50.0
        },
        {
            "event_id": "E3",
            "customer_id": "C2",
            "event_time": "2026-01-01T10:04:00",
            "amount": 75.0
        }
    ],
    "batch2.json": [
        {
            "event_id": "E4",
            "customer_id": "C1",
            "event_time": "2026-01-01T10:20:00",
            "amount": 200.0
        },
        {
            "event_id": "E5",
            "customer_id": "C2",
            "event_time": "2026-01-01T10:22:00",
            "amount": 125.0
        }
    ]
}

for filename, records in sample_data.items():
    file_path = INPUT_DIR / filename

    if not file_path.exists():
        with file_path.open("w", encoding="utf-8") as file:
            for record in records:
                file.write(json.dumps(record) + "\n")

print("Input files:", [p.name for p in INPUT_DIR.glob("*.json")])


schema = StructType([
    StructField("event_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("event_time", TimestampType(), True),
    StructField("amount", DoubleType(), True)
])


stream_df = (
    spark.readStream
    .format("json")
    .schema(schema)
    .option("maxFilesPerTrigger", 1)
    .load(str(INPUT_DIR.resolve()))
)

print("Streaming DataFrame:", stream_df.isStreaming)
stream_df.printSchema()


aggregated_df = (
    stream_df
    .withWatermark("event_time", "2 minutes")
    .groupBy(
        window(col("event_time"), "5 minutes"),
        col("customer_id")
    )
    .agg(
        spark_sum("amount").alias("total_amount")
    )
    .select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("customer_id"),
        col("total_amount")
    )
)


query = (
    aggregated_df.writeStream
    .format("parquet")
    .outputMode("append")
    .option("path", str(OUTPUT_DIR.resolve()))
    .option("checkpointLocation", str(CHECKPOINT_DIR.resolve()))
    .trigger(availableNow=True)
    .start()
)

query.awaitTermination()

print("Streaming query completed.")


if OUTPUT_DIR.exists() and any(OUTPUT_DIR.glob("*.parquet")):
    result_df = spark.read.parquet(str(OUTPUT_DIR.resolve()))
    print("Finalized window results:")
    result_df.orderBy("window_start", "customer_id").show(truncate=False)
else:
    print("No finalized windows were written in this run.")
    print(
        "Append mode waits for event-time progress to finalize windows. "
        "Add a later-event-time file and run again if needed."
    )


print("""
DECISION TABLE
--------------

Trigger:
1. availableNow=True
   - Processes available input and then stops.
   - Good for scheduled or periodic file ingestion.
   - Chosen for this assignment.

2. processingTime="10 seconds"
   - Keeps checking for new data at recurring intervals.
   - Better for a continuously running streaming pipeline.

Output mode:
1. Append
   - Writes only newly finalized rows.
   - Chosen for this watermarked window aggregation.

2. Update
   - Writes rows whose aggregate values changed.
   - Useful when consumers need interim updates.

3. Complete
   - Writes the entire aggregate result table each trigger.
   - Useful for small result tables, but can be expensive at scale.

Checkpoint:
- Tracks source progress and state for recovery.
- Use a dedicated checkpoint directory per query.
- Reuse it when restarting the same logical query.

Watermark:
- Tracks event-time progress, not wall-clock time.
- Bounds lateness/state retention for supported stateful operations.
- Events later than the watermark threshold may be dropped.
""")


spark.stop()
print("Assignment completed.")
