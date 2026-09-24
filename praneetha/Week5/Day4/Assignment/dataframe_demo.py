from pyspark.sql import SparkSession

spark = SparkSession.builder\
        .appName("DataFrameDemo")\
        .master("local[*]")\
        .getOrCreate()


data = [
    ("Arjun", 25, 30000),
    ("Priya", 30, 45000),
    ("Rahul", 28, 40000),
    ("Kavya", 35, 50000)
]

columns = ["name", "age", "salary"]

df = spark.createDataFrame(data,columns)

row = df.first()
print(row.name)
print(row.age)
df.show()

spark.stop()