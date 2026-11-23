from pyspark.sql import SparkSession
from pyspark.sql import functions as sf
from pyspark.sql.functions import spark_partition_id, count, lit , concat
from pyspark.sql.functions import udf
import random


spark = (
    SparkSession.builder
    .appName("salting-technique")
    .getOrCreate()
)

print(spark)

spark.conf.set("spark.sql.adaptive.enabled", False)
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", False)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)



_schema="first_name string,last_name string,job_title string,dob string,email string,phone string,salary double,department_id int"
emp_df=spark.read.format("csv").schema(_schema).options(header = True).load("employee_records.csv")

_dept_schema="department_id int,department_name string,description string,city string,state string,country string"
department_df=spark.read.format("csv").schema(_dept_schema).options(header = True).load("department_data.csv")


df_joined=emp_df.join(department_df , on="department_id" , how="left_outer")
df_joined.write.format("noop").mode("overwrite").save()
df_joined.show()
df_joined.explain()

part_df = df_joined.withColumn("partition_num", spark_partition_id()).groupBy("partition_num").agg(count(lit(1)).alias("count"))
part_df.show()


emp_df.groupBy("department_id").count().show()
spark.conf.set("spark.sql.shuffle.partitions", 32)


@udf
def salt_udf():
    return random.randint(0, 31)


salt_df = spark.range(0, 32)

salt_df.show()
salted_emp = emp_df.withColumn("salted_dept_id", concat("department_id", lit("_"), salt_udf()))

salted_emp.show() 

salted_dept = department_df.join(salt_df, how="cross").withColumn("salted_dept_id", concat("department_id", lit("_"), "id"))

salted_dept.where("department_id = 9").show()

# Lets make the salted join now
salted_joined_df = salted_emp.join(salted_dept, on=salted_emp.salted_dept_id==salted_dept.salted_dept_id, how="left_outer")

salted_joined_df.write.format("noop").mode("overwrite").save()

part_df = salted_joined_df.withColumn("partition_num", spark_partition_id()).groupBy("partition_num").agg(count(lit(1)).alias("count"))

part_df.show()




broadcast_joined_df = (emp_df.join(sf.broadcast(department_df), on="department_id", how="left_outer" ))

broadcast_joined_df.write.format("noop").mode("overwrite").save()
broadcast_joined_df.explain("formatted")




input("Press Enter to stop Spark...")

spark.stop()