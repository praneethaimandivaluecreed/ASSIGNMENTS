from pyspark.sql import SparkSession
from pyspark.sql.functions import avg



# 1. Create SparkSession

spark = (
    SparkSession.builder
    .appName("Day01_Pandas_vs_PySpark")
    .master("local[*]")
    .getOrCreate()
)
df = spark.read.csv("employees.csv", header=True, inferSchema=True)
df.show()



# 4. Filter employees
# Salary greater than 60,000

high_salary = df.filter(df.salary > 60000)

print("\n--- Employees with Salary > 60,000 ---")
high_salary.show()



# 5. Group by department
# and calculate average salary

department_salary = (
    df.groupBy("department")
      .agg(avg("salary").alias("average_salary"))
)



# 6. Sort by average salary

department_salary = department_salary.orderBy(
    "average_salary",
    ascending=False
)


print("\n--- Average Salary by Department ---")
department_salary.show()



# 7. Stop SparkSession

spark.stop()