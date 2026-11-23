
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SchemaDriftDemo")
    .master("local[2]")
    .getOrCreate()
)

# Batch 1: original schema
batch1 = spark.createDataFrame(
    [
        (25, "pikachu", 55),
        (1, "bulbasaur", 49)
    ],
    ["id", "name", "attack"]
)

# Batch 2: new schema with an extra column
batch2 = spark.createDataFrame(
    [
        (4, "charmander", 52, 43),
        (7, "squirtle", 48, 65)
    ],
    ["id", "name", "attack", "defense"]
)

# Write both batches separately
batch1.write.mode("overwrite").parquet(
    "data"
)

batch2.write.mode("overwrite").parquet(
    "data"
)

# Read all Parquet files using schema merging
merged_df = (
    spark.read
    .option("mergeSchema", "true")
    .parquet("data")
)

merged_df.printSchema()
merged_df.show()

input("\n press enter to stop spark \n")
spark.stop()
