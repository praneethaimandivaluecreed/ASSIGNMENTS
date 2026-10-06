from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField,
    IntegerType, StringType,
    DoubleType, DateType
)
from pyspark.sql import functions as F

# 1. SPARK SESSION

spark = (
    SparkSession.builder
    .appName("Day25_CustomerOrders_Analytics")
    .master("local[*]")
    .getOrCreate()
)



# 2. INPUT DATA

customers_data = [
    (1, "Alice", "Hyderabad"),
    (2, "Bob", "Chennai"),
    (3, "Charlie", "Bangalore"),
    (4, "David", "Hyderabad"),
    (5, "Eve", "Mumbai")
]

orders_data = [
    (101, 1, "2026-01-05", 500.0),
    (102, 1, "2026-01-10", 700.0),
    (103, 2, "2026-01-12", 300.0),
    (104, 2, "2026-01-15", 450.0),
    (105, 3, "2026-01-20", 1000.0),
    (106, 3, "2026-01-25", 250.0),
    (107, 4, "2026-02-01", 800.0),
    (108, 1, "2026-02-03", 200.0)
]

# 3. EXPLICIT SCHEMAS

customer_schema = StructType([
    StructField("customer_id", IntegerType(), False),
    StructField("customer_name", StringType(), False),
    StructField("city", StringType(), False)
])

order_schema = StructType([
    StructField("order_id", IntegerType(), False),
    StructField("customer_id", IntegerType(), False),
    StructField("order_date", StringType(), False),
    StructField("amount", DoubleType(), False)
])


customers = spark.createDataFrame(
    customers_data,
    customer_schema
)

orders = spark.createDataFrame(
    orders_data,
    order_schema
)

# 4. CONVERT ORDER DATE

orders = orders.withColumn(
    "order_date",
    F.to_date("order_date")
)



# 5. BASIC VALIDATION

assert customers.count() == 5, "Customer count is incorrect"
assert orders.count() == 8, "Order count is incorrect"

print("Input validation passed.")


# 6. INNER JOIN


inner_joined = (
    customers.alias("c")
    .join(
        orders.alias("o"),
        F.col("c.customer_id") == F.col("o.customer_id"),
        "inner"
    )
    .select(
        F.col("c.customer_id"),
        F.col("c.customer_name"),
        F.col("c.city"),
        F.col("o.order_id"),
        F.col("o.order_date"),
        F.col("o.amount")
    )
)

print("\n--- INNER JOIN ---")
inner_joined.show()

assert inner_joined.count() == 8, \
    "Inner join should contain 8 rows"

# 7. LEFT JOIN

left_joined = (
    customers.alias("c")
    .join(
        orders.alias("o"),
        F.col("c.customer_id") == F.col("o.customer_id"),
        "left"
    )
    .select(
        F.col("c.customer_id"),
        F.col("c.customer_name"),
        F.col("c.city"),
        F.col("o.order_id"),
        F.col("o.amount")
    )
)

print("\n--- LEFT JOIN ---")
left_joined.show()

# 8. CUSTOMER-LEVEL AGGREGATION

customer_analysis = (
    left_joined
    .groupBy(
        "customer_id",
        "customer_name",
        "city"
    )
    .agg(
        F.count("order_id").alias("order_count"),
        F.coalesce(
            F.sum("amount"),
            F.lit(0.0)
        ).alias("total_spend"),
        F.coalesce(
            F.avg("amount"),
            F.lit(0.0)
        ).alias("average_order_amount")
    )
    .orderBy("customer_id")
)

print("\n--- CUSTOMER ANALYSIS ---")
customer_analysis.show()

# 9. CUSTOMER-LEVEL VALIDATION


assert customer_analysis.count() == 5, \
    "Customer analysis should contain 5 customers"

alice = (
    customer_analysis
    .filter(F.col("customer_id") == 1)
    .first()
)

assert alice["order_count"] == 3
assert alice["total_spend"] == 1400.0

eve = (
    customer_analysis
    .filter(F.col("customer_id") == 5)
    .first()
)

assert eve["order_count"] == 0
assert eve["total_spend"] == 0.0

print("Customer aggregation validation passed.")

# 10. CITY-LEVEL AGGREGATION

city_analysis = (
    customer_analysis
    .groupBy("city")
    .agg(
        F.count("customer_id").alias("customer_count"),
        F.sum("order_count").alias("total_orders"),
        F.sum("total_spend").alias("total_revenue"),
        F.avg("total_spend").alias("average_customer_spend")
    )
    .orderBy("city")
)

print("\n--- CITY ANALYSIS ---")
city_analysis.show()

# 11. CITY VALIDATION


assert city_analysis.count() == 4, \
    "There should be 4 cities"

print("City aggregation validation passed.")

# 12. EXECUTION PLAN


print("\n--- EXECUTION PLAN ---")
customer_analysis.explain("formatted")

# 13. STOP SPARK


spark.stop()