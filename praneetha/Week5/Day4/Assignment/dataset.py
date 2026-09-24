from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("DataFramePipeline") \
    .master("local[*]") \
    .getOrCreate()


# data


data = [
    ("Arjun", "HR", "30000"),
    ("Priya", "IT", "45000"),
    ("Rahul", "HR", "35000"),
    ("Kavya", "IT", "50000")
]

raw_df = spark.createDataFrame(
    data,
    ["name", "department", "salary"]
)

print("RAW DATA")
raw_df.show()



# Type conversion


typed_df = raw_df.withColumn(
    "salary",
    col("salary").cast("int")
)

print("TYPED DATA")
typed_df.printSchema()
typed_df.show()



# Validation


valid_df = typed_df.filter(
    col("name").isNotNull() &
    col("department").isNotNull() &
    col("salary").isNotNull() &
    (col("salary") >= 0)
)

invalid_df = typed_df.filter(
    col("name").isNull() |
    col("department").isNull() |
    col("salary").isNull() |
    (col("salary") < 0)
)



# creating a new df


result_df = valid_df \
    .filter(col("salary") >= 40000) \
    .withColumn(
        "salary_after_bonus",
        col("salary") * 1.10
    )



# printing


print("VALID DATA")
valid_df.show()

print("INVALID DATA")
invalid_df.show()

print("FINAL RESULT")
result_df.show()


spark.stop()