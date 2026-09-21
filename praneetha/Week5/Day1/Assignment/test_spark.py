from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("FirstSparkJob") \
    .getOrCreate()

data = [
    ("Praneetha", 85),
    ("Rahul", 72),
    ("Kavya", 91),
    ("Niha", 65)
]

df = spark.createDataFrame(
    data,
    ["name", "marks"]
)

result = df.filter(df["marks"] >= 80)

result.show()

spark.stop()