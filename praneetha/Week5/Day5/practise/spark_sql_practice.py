from pyspark.sql import SparkSession

spark = SparkSession.builder\
        .appName("sql practise")\
        .master("local[*]")\
        .getOrCreate()


data = [
    (1, "Praneetha", "IT", 60000),
    (2, "Rahul", "HR", 45000),
    (3, "Kavya", "IT", 70000),
    (4, "Niha", "HR", 50000),
    (5, "Arjun", "IT", 55000),
    (6, "Bhavana", "Finance", 65000),
    (7, "Ravi", "Finance", 55000),
    (8, "Sneha", "HR", 48000),
    (9, "Kiran", "IT", 70000),
    (10, "Anu", "Finance", 60000)
]

columns = ["id", "name", "department", "salary"]

df = spark.createDataFrame(data, columns)

df.show()

# CREATING A VIEW
df.createOrReplaceTempView("employees")

# using employees view
result = spark.sql("""
    SELECT
        name,
        department,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department
            ORDER BY salary DESC
        ) AS salary_rank
    FROM employees
""")

result.show()
spark.stop()