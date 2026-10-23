import os
from datetime import datetime
import pandas as pd

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    DoubleType
)


# cerating spark sesion

spark = (
    SparkSession.builder
    .appName("Incremental Load Project")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# Get the folder in which this Python file is saved
project_path = os.path.dirname(os.path.abspath(__file__))

# Source data
source_path = os.path.join(project_path, "orders.csv")

# Folder where processed data will be stored
output_folder = os.path.join(project_path, "output")
target_path = os.path.join(output_folder, "orders_target.csv")

# File that stores the last successfully processed timestamp
checkpoint_path = os.path.join(
    output_folder, "orders_watermark.txt"
)

# Create the output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)


# defining the schema

orders_schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_id", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("status", StringType(), True),
    StructField("updated_at", StringType(), True),
    StructField("source_sequence", IntegerType(), True)
])


# reading the source data

if not os.path.exists(source_path):
    raise FileNotFoundError(
        f"Source file not found: {source_path}"
    )

source_df = (
    spark.read
    .option("header", True)
    .schema(orders_schema)
    .csv(source_path)
)

# Convert the timestamp string into a timestamp column
source_df = source_df.withColumn(
    "updated_at",
    F.to_timestamp("updated_at", "yyyy-MM-dd HH:mm:ss")
)

# Stop if timestamps are missing or invalid
invalid_timestamp_count = (
    source_df.filter(F.col("updated_at").isNull()).count()
)

if invalid_timestamp_count > 0:
    raise ValueError(
        f"Found {invalid_timestamp_count} rows with invalid timestamps"
    )

# Stop if the business key is missing
if source_df.filter(F.col("order_id").isNull()).count() > 0:
    raise ValueError("Null order_id found in source data")


# reading the watermark

# The first run starts from an old timestamp
if os.path.exists(checkpoint_path):
    with open(checkpoint_path, "r") as file:
        last_watermark = file.read().strip()
else:
    last_watermark = "1900-01-01 00:00:00"

print("Previous watermark:", last_watermark)



# identifying the current batch
# Find the latest timestamp available in the source
batch_upper_bound = (
    source_df
    .agg(F.max("updated_at").alias("max_updated_at"))
    .first()["max_updated_at"]
)

if batch_upper_bound is None:
    print("No source data available.")

elif batch_upper_bound <= datetime.strptime(
    last_watermark, "%Y-%m-%d %H:%M:%S"
):
    # Do not move the watermark backwards
    print("No new data to process.")

else:
    # Process records after the previous watermark
    # and up to the current batch boundary
    incremental_df = source_df.filter(
        (F.col("updated_at") > F.to_timestamp(
            F.lit(last_watermark)
        ))
        & (F.col("updated_at") <= F.lit(batch_upper_bound))
    )

    print("Incoming rows:", incremental_df.count())


 
    # de duplicating 
    # Keep the latest version of each order.
    # source_sequence resolves records with matching timestamps.
    window_spec = (
        Window
        .partitionBy("order_id")
        .orderBy(
            F.col("updated_at").desc(),
            F.col("source_sequence").desc()
        )
    )

    deduplicated_df = (
        incremental_df
        .withColumn(
            "row_num",
            F.row_number().over(window_spec)
        )
        .filter(F.col("row_num") == 1)
        .drop("row_num")
    )

    print("Rows after deduplication:", deduplicated_df.count())


   # merging with exisisting data

    if deduplicated_df.count() > 0:

        if os.path.exists(target_path):
            # Read the existing target using Pandas to avoid Windows Hadoop/Winutils issues
            target_pandas_df = pd.read_csv(target_path)
            target_df = spark.createDataFrame(target_pandas_df)

            target_df = target_df.withColumn(
                "updated_at",
                F.to_timestamp("updated_at", "yyyy-MM-dd HH:mm:ss")
            )

            # Keep old orders that are not being updated
            unchanged_df = target_df.join(
                deduplicated_df
                .select("order_id")
                .distinct(),
                on="order_id",
                how="left_anti"
            )

            # Add the latest incoming versions
            final_df = unchanged_df.unionByName(
                deduplicated_df
            )

        else:
            # First successful load
            final_df = deduplicated_df


        # validating the final data

        if final_df.filter(
            F.col("order_id").isNull()
        ).count() > 0:
            raise ValueError("Null order_id found in target data")

        duplicate_keys = (
            final_df
            .groupBy("order_id")
            .count()
            .filter(F.col("count") > 1)
        )

        if duplicate_keys.count() > 0:
            duplicate_keys.show(truncate=False)
            raise ValueError(
                "Duplicate order_id found in final data"
            )


     

        # Save the target first using Pandas.
        # Update the watermark only after the write succeeds.
        pandas_final_df = final_df.toPandas()
        pandas_final_df.to_csv(target_path, index=False)

        print("Target data written successfully.")


        # updating the watermark
        new_watermark = batch_upper_bound.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(checkpoint_path, "w") as file:
            file.write(new_watermark)

        print("New watermark:", new_watermark)
        print("Incremental load completed successfully.")

        # Display the final result
        final_df.orderBy("order_id").show(truncate=False)

    else:
        print("No records in the incoming batch.")


spark.stop()