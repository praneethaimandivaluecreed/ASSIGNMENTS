from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("SparkUIPractice")
    .master("local[*]")
    .getOrCreate()
)

df = (
    spark.range(0, 1_000_000)
    .withColumn("group_id", F.col("id") % 100)
)

result = (
    df.groupBy("group_id")
      .agg(F.count("*").alias("cnt"))
)

result.show()
input("Press Enter to stop Spark...")

spark.stop()
