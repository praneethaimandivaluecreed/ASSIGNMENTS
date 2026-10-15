from pathlib import Path
from datetime import datetime, timedelta
import json
import shutil

from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, IntegerType, StringType, TimestampType
)

# ============================================================
# CONFIGURATION
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
SOURCE_FILE = BASE_DIR / "data" / "source" / "customers.csv"
WAREHOUSE_DIR = BASE_DIR / "data" / "warehouse"

SCD1_PATH = WAREHOUSE_DIR / "customers_scd1"
SCD2_PATH = WAREHOUSE_DIR / "customers_scd2"
STATE_FILE = WAREHOUSE_DIR / "watermark.json"

MODE = "incremental"       # "incremental" or "backfill"
OVERLAP_HOURS = 48

# For bounded backfills. The sample's SCD2 rebuild below uses all
# source history, which is safer than rebuilding from a partial slice.
BACKFILL_START = "2026-10-01 00:00:00"
BACKFILL_END = "2026-10-31 23:59:59"

WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

spark = (
    SparkSession.builder
    .appName("Day37_Incremental_Loads")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")


# ============================================================
# SOURCE SCHEMA AND READ
# ============================================================
SOURCE_SCHEMA = StructType([
    StructField("customer_id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("city", StringType(), True),
    StructField("updated_at", StringType(), True),
    StructField("source_sequence", IntegerType(), True),
])


def read_source():
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(
            f"Source file not found: {SOURCE_FILE}\n"
            "Place customers.csv under data/source/."
        )

    df = (
        spark.read
        .option("header", True)
        .schema(SOURCE_SCHEMA)
        .csv(str(SOURCE_FILE))
        .withColumn(
            "updated_at",
            F.to_timestamp("updated_at", "yyyy-MM-dd HH:mm:ss")
        )
    )

    invalid = df.filter(
        F.col("customer_id").isNull()
        | F.col("updated_at").isNull()
        | F.col("source_sequence").isNull()
    )

    if invalid.limit(1).count():
        invalid.show(truncate=False)
        raise ValueError("Invalid customer_id, updated_at, or source_sequence.")

    # Remove exact duplicate events; distinct versions remain.
    return df.dropDuplicates([
        "customer_id", "name", "city", "updated_at", "source_sequence"
    ])


# ============================================================
# WATERMARK CHECKPOINT
# ============================================================
def read_watermark():
    if not STATE_FILE.exists():
        return None
    with STATE_FILE.open("r", encoding="utf-8") as f:
        value = json.load(f).get("watermark")
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def write_watermark(value):
    # Write temp file first, then rename. This protects the JSON file
    # from being left partially written; it is not a data transaction.
    temp_path = STATE_FILE.with_suffix(".tmp")
    with temp_path.open("w", encoding="utf-8") as f:
        json.dump(
            {"watermark": value.strftime("%Y-%m-%d %H:%M:%S")},
            f,
            indent=2
        )
    temp_path.replace(STATE_FILE)


# ============================================================
# DEDUPLICATION: LATEST RECORD PER BUSINESS KEY
# ============================================================
def latest_per_customer(df):
    w = (
        Window.partitionBy("customer_id")
        .orderBy(
            F.col("updated_at").desc(),
            F.col("source_sequence").desc(),
            F.col("name").desc_nulls_last(),
            F.col("city").desc_nulls_last()
        )
    )
    return (
        df.withColumn("_rn", F.row_number().over(w))
        .filter(F.col("_rn") == 1)
        .drop("_rn")
    )


# ============================================================
# SCD TYPE 1 UPSERT
# Keep only the latest state; no business history.
# ============================================================
def upsert_scd1(incoming):
    if incoming.limit(1).count() == 0:
        print("SCD1: no incoming records.")
        return

    incoming = latest_per_customer(incoming)

    if not SCD1_PATH.exists():
        incoming.write.mode("overwrite").parquet(str(SCD1_PATH))
        print("SCD1 initialized.")
        return

    target = spark.read.parquet(str(SCD1_PATH)).alias("t")
    src = incoming.alias("s")

    joined = src.join(
        target.select(
            "customer_id",
            F.col("updated_at").alias("_target_updated_at"),
            F.col("source_sequence").alias("_target_sequence")
        ).alias("t"),
        on="customer_id",
        how="left"
    )

    newer = joined.filter(
        F.col("_target_updated_at").isNull()
        | (F.col("s.updated_at") > F.col("_target_updated_at"))
        | (
            (F.col("s.updated_at") == F.col("_target_updated_at"))
            & (F.col("s.source_sequence") > F.col("_target_sequence"))
        )
    ).select("s.*")

    # Keep target keys that do not appear in the accepted incoming rows.
    retained = target.join(
        newer.select("customer_id").distinct(),
        on="customer_id",
        how="left_anti"
    ).select(
        "t.customer_id", "t.name", "t.city",
        "t.updated_at", "t.source_sequence"
    )

    result = retained.unionByName(newer)

    # Local learning implementation only. Parquet overwrite is not
    # transactional; production needs atomic publication/table format.
    result.write.mode("overwrite").parquet(str(SCD1_PATH))
    print("SCD1 upsert complete.")


# ============================================================
# SCD TYPE 2 HISTORY MERGE
# Preserve each meaningful customer state as a version.
# ============================================================
def make_scd2(history):
    # Resolve multiple events with the same customer/timestamp by
    # choosing the highest source_sequence deterministically.
    same_time = (
        Window.partitionBy("customer_id", "updated_at")
        .orderBy(
            F.col("source_sequence").desc(),
            F.col("name").desc_nulls_last(),
            F.col("city").desc_nulls_last()
        )
    )

    events = (
        history.dropDuplicates([
            "customer_id", "name", "city", "updated_at", "source_sequence"
        ])
        .withColumn("_rn", F.row_number().over(same_time))
        .filter(F.col("_rn") == 1)
        .drop("_rn")
    )

    order_w = Window.partitionBy("customer_id").orderBy(
        "updated_at", "source_sequence"
    )

    # Don't create a new version when only the event metadata changes
    # but the tracked attributes (name/city) stay the same.
    events = (
        events
        .withColumn("_prev_name", F.lag("name").over(order_w))
        .withColumn("_prev_city", F.lag("city").over(order_w))
        .withColumn(
            "_changed",
            F.col("_prev_name").isNull()
            | (~F.col("name").eqNullSafe(F.col("_prev_name")))
            | (~F.col("city").eqNullSafe(F.col("_prev_city")))
        )
        .filter(F.col("_changed"))
        .drop("_prev_name", "_prev_city", "_changed")
    )

    timeline_w = Window.partitionBy("customer_id").orderBy(
        "updated_at", "source_sequence"
    )

    return (
        events
        .withColumn("valid_from", F.col("updated_at"))
        .withColumn("valid_to", F.lead("updated_at").over(timeline_w))
        .withColumn("is_current", F.col("valid_to").isNull())
        .select(
            "customer_id", "name", "city",
            "updated_at", "source_sequence",
            "valid_from", "valid_to", "is_current"
        )
    )


def upsert_scd2(full_source_history):
    # For this assignment, rebuild the SCD2 target from complete source
    # history. It is deterministic and replay-safe, but less efficient
    # than merging only changed keys for large datasets.
    scd2 = make_scd2(full_source_history)
    scd2.write.mode("overwrite").parquet(str(SCD2_PATH))
    print("SCD2 history rebuilt.")


# ============================================================
# VALIDATION
# ============================================================
def validate_outputs():
    scd1 = spark.read.parquet(str(SCD1_PATH))
    scd2 = spark.read.parquet(str(SCD2_PATH))

    duplicate_scd1 = (
        scd1.groupBy("customer_id")
        .count()
        .filter(F.col("count") > 1)
    )
    if duplicate_scd1.limit(1).count():
        duplicate_scd1.show(truncate=False)
        raise AssertionError("SCD1 has duplicate customer keys.")

    invalid_scd2 = scd2.groupBy("customer_id").agg(
        F.sum(F.col("is_current").cast("int")).alias("current_count")
    ).filter(F.col("current_count") != 1)

    if invalid_scd2.limit(1).count():
        invalid_scd2.show(truncate=False)
        raise AssertionError("Each SCD2 customer must have exactly one current row.")

    invalid_intervals = scd2.filter(
        F.col("valid_to").isNotNull()
        & (F.col("valid_to") <= F.col("valid_from"))
    )
    if invalid_intervals.limit(1).count():
        invalid_intervals.show(truncate=False)
        raise AssertionError("SCD2 contains invalid validity intervals.")

    print("Validation passed.")
    print("SCD1 rows:", scd1.count())
    print("SCD2 rows:", scd2.count())


# ============================================================
# INCREMENTAL / BACKFILL ORCHESTRATION
# ============================================================
def main():
    source = read_source()

    if MODE == "backfill":
        start = datetime.strptime(BACKFILL_START, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(BACKFILL_END, "%Y-%m-%d %H:%M:%S")
        if start > end:
            raise ValueError("BACKFILL_START must be <= BACKFILL_END")

        # For this demo, the CSV is the complete event history.
        # Rebuild both tables from all history for consistent results.
        # Do not advance the normal incremental watermark.
        upsert_scd1(latest_per_customer(source))
        upsert_scd2(source)
        validate_outputs()
        print("Full-history replay completed; watermark unchanged.")
        return

    if MODE != "incremental":
        raise ValueError("MODE must be 'incremental' or 'backfill'.")

    previous = read_watermark()

    if previous is None:
        incoming = source
    else:
        lower_bound = previous - timedelta(hours=OVERLAP_HOURS)
        incoming = source.filter(F.col("updated_at") >= F.lit(lower_bound))

    max_ts = incoming.agg(F.max("updated_at").alias("max_ts")).first()["max_ts"]

    if max_ts is None:
        print("No records found for this run.")
        return

    print("Previous watermark:", previous)
    print("Selected max timestamp:", max_ts)
    print("Incoming source rows:", incoming.count())

    # Build/merge data outputs first. Only update watermark after both
    # writes and validations succeed. Parquet output writes themselves
    # are not a multi-table transaction.
    upsert_scd1(latest_per_customer(incoming))
    upsert_scd2(source)
    validate_outputs()

    # Never move the watermark backwards.
    if previous is not None and max_ts < previous:
        max_ts = previous

    write_watermark(max_ts)
    print("Watermark committed:", max_ts)
    print("Incremental pipeline completed successfully.")


if __name__ == "__main__":
    try:
        main()
    finally:
        spark.stop()
