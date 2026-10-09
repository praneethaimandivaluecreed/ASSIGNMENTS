from pyspark.sql import SparkSession,functions as f

spark = SparkSession.builder\
                 .appName("Skewed_join")\
                .master("local[*]")\
                .getOrCreate()
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
orders = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/orders_skewed.csv")
)

customers = (
    spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("data/customers.csv")
)

print("customers Schema: ")
customers.printSchema()

print("Orders Schema: ")
orders.printSchema()

print("Customers count: ",customers.count())
print("Orders count: ",orders.count())

#Checking whether data contains hot keys

customer_orders = (orders.groupBy('customer_id')
                   .count()
                   .orderBy(f.desc("count")))
customer_orders.show(10)

# #implementing the base join

# base_join = orders.join(customers,on="customer_id",how='inner')

# base_join.count()
# base_join.explain("formatted")

broadcast_join = orders.join(
    f.broadcast(customers),
    on="customer_id",
    how="inner"
)

broadcast_join.count()

broadcast_join.explain("formatted")

input("Press Enter to stop Spark...")
spark.stop()