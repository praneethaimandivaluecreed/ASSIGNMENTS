from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Creates the intentionally poor input dataset for the redesign exercise.
# Run from the project directory containing data/sample_shows.csv.
INPUT_CSV = "data/sample_shows.csv"
OUTPUT_PARQUET = "data/poor_parquet"

spark = (
    SparkSession.builder
    .appName("GeneratePoorParquetPracticeData")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

try:
    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(INPUT_CSV)
    )

    # Make the output deliberately poor:
    # show_id is nearly unique, so partitionBy creates many directories
    # with very little data per directory.
    (
        df.repartition(8)
        .write
        .mode("overwrite")
        .option("compression", "snappy")
        .partitionBy("show_id")
        .parquet(OUTPUT_PARQUET)
    )

    print(f"Created intentionally poor Parquet dataset: {OUTPUT_PARQUET}")
    print(f"Rows: {spark.read.parquet(OUTPUT_PARQUET).count():,}")
    print("Inspect the folder: it should contain many show_id=... directories.")
finally:
    spark.stop()
