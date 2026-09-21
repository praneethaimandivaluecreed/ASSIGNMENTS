from pyspark.sql import SparkSession
from pyspark.sql.functions import avg,round

#setting spark session
spark = (
    SparkSession.builder.
    appName("average_salary_spark")
    .master('local[*]')
    .getOrCreate()
)

data = [
    (101,'IT',60000),
    (102,'HR',50000),
    (103,'IT',80000),
    (104,'Finance',70000),
    (105,'IT',65000)
]
columns = ['employee_id','department','salary']

#creating a pandas dataframe
df = spark.createDataFrame(data,columns)
df.show()

#finding average salary for each department

df1 = (df.groupBy('department').agg(round(avg('salary'),2).alias("average_salary")))
df1.show()

spark.stop() # closing the spark session