from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, count, sum, avg, dense_rank
)
from pyspark.sql.window import Window

spark = (
    SparkSession.builder
    .appName("Day23_Practical")
    .master("local[*]")
    .getOrCreate()
)

employee_data = [
    (101, "Rahul", "IT", 60000),
    (102, "Priya", "HR", 50000),
    (103, "Arjun", "IT", 70000),
    (104, "Sneha", "Finance", 65000),
    (105, "Vikram", "HR", 55000),
    (106, "Anita", "IT", 80000),
    (107, "Kiran", "Finance", 72000),
    (108, "Meena", "Sales", 48000),
    (109, "Ravi", "Sales", 52000),
    (110, "Divya", "IT", 70000)
]

employees = spark.createDataFrame(
    employee_data,
    ["employee_id", "name", "department", "salary"]
)

department_data = [
    ("IT", "Technology"),
    ("HR", "Human Resources"),
    ("Finance", "Finance"),
    ("Sales", "Sales"),
    ("Marketing", "Marketing")
]

departments = spark.createDataFrame(
    department_data,
    ["department", "department_name"]
)


employees.show()
employees.printSchema()
print("Employee count:", employees.count())

employees_band = employees.withColumn(
    "salary_band",
    when(col("salary") >= 75000, "High")
    .when(col("salary") >= 60000, "Medium")
    .otherwise("Low")
)

employees_band.filter(
    col("salary") > 55000
).select(
    "employee_id",
    "name",
    "department",
    "salary",
    "salary_band"
).show()



department_summary = (
    employees
    .groupBy("department")
    .agg(
        count("*").alias("employee_count"),
        sum("salary").alias("total_salary"),
        avg("salary").alias("average_salary")
    )
    .orderBy(col("total_salary").desc())
)

department_summary.show()




joined = (
    employees.alias("e")
    .join(
        departments.alias("d"),
        col("e.department") == col("d.department"),
        "left"
    )
    .select(
        col("e.employee_id"),
        col("e.name"),
        col("e.department"),
        col("d.department_name"),
        col("e.salary")
    )
)

joined.show()


salary_window = Window.partitionBy(
    "department"
).orderBy(
    col("salary").desc()
)

ranked = employees.withColumn(
    "salary_rank",
    dense_rank().over(salary_window)
)

ranked.show()


employees.createOrReplaceTempView("employees")

sql_result = spark.sql("""
    SELECT
        department,
        COUNT(*) AS employee_count,
        AVG(salary) AS average_salary
    FROM employees
    GROUP BY department
    ORDER BY average_salary DESC
""")

sql_result.show()


print("========== AGGREGATION PLAN ==========")

department_summary.explain("formatted")


print("========== JOIN PLAN ==========")

joined.explain("formatted")


print("========== WINDOW PLAN ==========")

ranked.explain("formatted")


spark.stop()