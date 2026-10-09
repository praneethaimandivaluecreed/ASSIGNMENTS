from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum

spark = (
    SparkSession.builder
    .appName("SparkUIExample")
    .master("local[*]")
    .getOrCreate()
)

df = spark.read.csv(
    "sales.csv",
    header=True,
    inferSchema=True
)

result = (
    df
    .filter(col("amount") > 1000)
    .groupBy("department")
    .agg(sum("amount").alias("total_sales"))
)

result.show()
input("Press Enter to stop Spark...")