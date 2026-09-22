from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SalesAnalysis")
    .master("local[4]")
    .getOrCreate()
)

# Read the CSV
df = spark.read.csv(
    "sales.csv",
    header=True,
    inferSchema=True
)

print("Original Data:")
df.show()

# Transformation 1 - narrow
filtered_df = df.filter(df.amount > 10000)

# Transformation 2 - wide
result = (
    filtered_df
    .groupBy("city")
    .sum("amount")
)

print("Final Result:")
result.show()

print("Application is still running...")
input("Press Enter to stop Spark...")

spark.stop()