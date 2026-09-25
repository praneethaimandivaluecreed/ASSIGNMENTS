from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("RDDSolution")
    .master("local[*]")
    .getOrCreate()
)

sc = spark.sparkContext

data = [
    (101, "Rahul", "IT", 60000),
    (102, "Priya", "HR", 50000),
    (103, "Amit", "IT", 80000),
    (104, "Neha", "Finance", 70000),
    (105, "Arjun", "IT", 70000)
]

employees = sc.parallelize(data)

filtered = employees.filter(
    lambda row: row[3] > 55000
)

department_salary = filtered.map(
    lambda row: (row[2], row[3])
)

department_groups = department_salary.groupByKey()

result = department_groups.map(
    lambda x: (
        x[0],
        sum(x[1]) / len(x[1])
    )
)

for row in result.collect():
    print(row)

spark.stop()