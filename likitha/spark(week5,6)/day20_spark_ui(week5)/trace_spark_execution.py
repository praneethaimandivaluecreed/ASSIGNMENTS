from pyspark.sql import SparkSession
from pyspark.sql.functions import avg



# Create Spark Session
spark = (
    SparkSession.builder
    .appName("Day02_Spark_Execution_Trace")
    .master("local[4]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")



# Create sample employee data
data = [
    (1, "Alice", "IT", 60000),
    (2, "Bob", "HR", 50000),
    (3, "Charlie", "IT", 75000),
    (4, "David", "Sales", 55000),
    (5, "Eve", "HR", 65000),
    (6, "Frank", "IT", 80000),
    (7, "Grace", "Sales", 60000),
    (8, "Henry", "HR", 70000),
    (9, "Ivy", "IT", 72000),
    (10, "Jack", "Sales", 58000),
    (11, "Kate", "HR", 62000),
    (12, "Leo", "IT", 68000),
]


columns = [
    "employee_id",
    "name",
    "department",
    "salary"
]


df = spark.createDataFrame(data, columns)



# Check partitions
print("\nNumber of partitions:")
print(df.rdd.getNumPartitions())



# Transformation
filtered_df = df.filter(df.salary > 60000)

print("\nFiltered DataFrame created.")
print("At this point, Spark has only built the execution plan.")



# Shuffle transformation
department_salary = (
    filtered_df
    .groupBy("department")
    .agg(
        avg("salary").alias("average_salary")
    )
)


print("\nGroupBy transformation created.")
print("This operation introduces a shuffle boundary.")



# ACTION
print("\nExecuting Spark job...\n")

department_salary.show()



#  Another action
print("\nCounting final records...\n")

count = department_salary.count()

print("Final record count:", count)



# Keep application alive briefly
input("\nPress ENTER to stop Spark...")


spark.stop()