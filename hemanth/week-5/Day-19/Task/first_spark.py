from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.
    appName("first_spark").
    master("local[*]").
    getOrCreate()
)

spark.range(20).show()