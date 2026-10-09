from pyspark.sql import SparkSession
from pyspark.sql.functions import col, broadcast, lit, concat, floor, rand, when, count, broadcast
#from pyspark.sql.dataframe import join

spark = (
    SparkSession.builder
    .appName("SkewedJoinOptimization")
    .master("local[*]")
    .getOrCreate()
)

# reading the files and creating spark dataframe  out of them
customers = spark.read.option("header",True).option("inferSchema", True).csv('C:/Users/VC_User6.DESKTOP-22FFUC4/Desktop/DATA ANALYTICS/ASSIGNMENTS/praneetha/Week7/Day4/Assignment/customers.csv')
orders = spark.read.option("header", True).option("inferSchema", True).csv("C:/Users/VC_User6.DESKTOP-22FFUC4/Desktop/DATA ANALYTICS/ASSIGNMENTS/praneetha/Week7/Day4/Assignment/orders.csv")


spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)


# showing the dataframes
customers.show()
orders.show()

# printing the schema of the spark dataframes
customers.printSchema()
orders.printSchema()


# joining both tables (customers & orders) based on customer_id
combined_df = customers.join(orders , on = 'customer_id', how = "inner")
combined_df.show()

# checking how the process executed
combined_df.explain('formatted') 
# found out that spark is already using brodcast join


# checking the customer distribution among the data
customer_distribution = (
    orders
    .groupBy("customer_id")
    .agg(count("*").alias("order_count"))
    .orderBy(col("order_count").desc())
)


customer_distribution.show()

# explicitly mentioning brodcast
broadcast_join_df = orders.join(
    broadcast(customers),
    on="customer_id",
    how="inner"
)
broadcast_join_df.show()
broadcast_join_df.explain('formatted')



# SALTING


SALT_COUNT = 10
HOT_CUSTOMER = "999999"

#Add random salt to orders
salted_orders = orders.withColumn(
    "salt",
    when(
        col("customer_id") == HOT_CUSTOMER,
        floor(rand() * SALT_COUNT).cast("int")
    ).otherwise(lit(0))
)

# Create salted customer_id


salted_orders = salted_orders.withColumn(
    "salted_customer_id",
    concat(
        col("customer_id"),
        lit("_"),
        col("salt")
    )
)

# Create salt values


salt_values = spark.range(SALT_COUNT).withColumnRenamed(
    "id",
    "salt"
)

# Create salted customer table

salted_customers = (
    customers
    .crossJoin(salt_values)
    .withColumn(
        "salted_customer_id",
        concat(
            col("customer_id"),
            lit("_"),
            col("salt")
        )
    )
)

#Salted join
salted_join_df = salted_orders.join(
    salted_customers,
    on="salted_customer_id",
    how="inner"
)

#Check physical plan
salted_join_df.explain("formatted")
input("Press Enter to stop Spark...")
