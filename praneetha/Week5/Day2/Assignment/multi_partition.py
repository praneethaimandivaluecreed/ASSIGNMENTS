from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = (
    SparkSession.builder
    .appName("MultiPartitionDemo")
    .master("local[4]")
    .config("spark.sql.adaptive.enabled", "false")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Create 100,000 rows in 4 partitions
df = spark.range(
    start=1,
    end=100001,
    numPartitions=4
)

# Add some realistic columns
df = (
    df
    .withColumn("amount", (col("id") % 5000) + 1000)
    .withColumn(
        "city",
        when(col("id") % 3 == 0, "Hyderabad")
        .when(col("id") % 3 == 1, "Chennai")
        .otherwise("Mumbai")
    )
)

print("\nNumber of partitions:")
print(df.rdd.getNumPartitions())

print("\nSample data:")
df.show(10)

# Narrow transformations
filtered_df = df.filter(col("amount") > 3000)

# Wide transformation -> shuffle
result = (
    filtered_df
    .groupBy("city")
    .sum("amount")
)

print("\nFinal Result:")
result.show()

print("\nApplication is still running...")
input("Press Enter to stop Spark...")

spark.stop()