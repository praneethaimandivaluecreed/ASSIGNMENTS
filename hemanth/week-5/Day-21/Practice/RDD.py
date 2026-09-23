from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("RDD_Testing").master('local[*]').getOrCreate()
)

numbers = [10, 20, 30, 40, 50, 60]

rdd = spark.sparkContext.parallelize(numbers,3)

print("Number of partitions: ",rdd.getNumPartitions())

rdd1 = rdd.map(lambda x : x*2)
print("Transformed RDD 1 :",rdd1.collect())

rdd2 = rdd1.filter(lambda x : x > 60)
print("Transformed RDD 1=2 :",rdd2.collect())

input("Enter a key to stop the spark")
spark.stop()