from pyspark.sql import SparkSession
from pyspark.sql.functions import avg

spark = (
    SparkSession.builder
    .appName("SparkTrace")
    .master("local[*]")
    .getOrCreate()
)

print("=== APPLICATION STARTED ===")

data = [
    (101, "IT", 60000),
    (102, "HR", 50000),
    (103, "IT", 80000),
    (104, "Finance", 70000),
    (105, "IT", 65000),
    (106, "HR", 55000),
    (107, "Finance", 75000),
    (108, "IT", 70000),
]

columns = ["employee_id", "department", "salary"]

df = spark.createDataFrame(data, columns)

print("=== DATAFRAME CREATED ===")

df_filtered = df.filter(df.salary > 55000)

print("=== FILTER CREATED ===")

df_grouped = (
    df_filtered
    .groupBy("department")
    .agg(avg("salary").alias("average_salary"))
)

print("=== GROUPBY PLAN CREATED ===")

print("=== ACTION 1: SHOW ===")
df_grouped.show()

print("=== ACTION 2: COUNT ===")
count = df_grouped.count()

print(f"Result count: {count}")

print("=== APPLICATION END ===")

spark.stop()