from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    sum,
    row_number,
    lag,
    dense_rank
)
from pyspark.sql.window import Window



# SPARK SESSION


spark = (
    SparkSession.builder
    .appName("Day26_Window_Functions_Assignment")
    .master("local[*]")
    .getOrCreate()
)



# PROBLEM 1 — LATEST CUSTOMER RECORD


customer_data = [
    (101, "Alice", "Hyderabad", "2026-01-10 09:00:00"),
    (101, "Alice", "Bangalore", "2026-02-15 10:30:00"),
    (101, "Alice", "Chennai", "2026-03-20 14:00:00"),

    (102, "Bob", "Delhi", "2026-01-05 11:00:00"),
    (102, "Bob", "Mumbai", "2026-02-10 15:00:00"),

    (103, "Charlie", "Pune", "2026-03-01 08:00:00")
]

customer_df = spark.createDataFrame(
    customer_data,
    ["customer_id", "customer_name", "city", "updated_at"]
)


print("Latest Customer Record")

customer_window = (
    Window
    .partitionBy("customer_id")
    .orderBy(col("updated_at").desc())
)

latest_customer_df = (
    customer_df
    .withColumn(
        "row_num",
        row_number().over(customer_window)
    )
    .filter(col("row_num") == 1)
    .drop("row_num")
)

latest_customer_df.show(truncate=False)



# PROBLEM 2 — TOP 2 PRODUCTS PER CATEGORY


sales_data = [
    ("Electronics", "Laptop", 50000),
    ("Electronics", "Phone", 30000),
    ("Electronics", "Tablet", 20000),
    ("Electronics", "Monitor", 15000),

    ("Furniture", "Chair", 10000),
    ("Furniture", "Table", 25000),
    ("Furniture", "Sofa", 40000),
    ("Furniture", "Bed", 35000),

    ("Clothing", "Shirt", 12000),
    ("Clothing", "Jeans", 18000),
    ("Clothing", "Jacket", 25000),
    ("Clothing", "Shoes", 30000)
]

sales_df = spark.createDataFrame(
    sales_data,
    ["category", "product", "amount"]
)


print("Top 2 Products Per Category")


product_sales_df = (
    sales_df
    .groupBy("category", "product")
    .agg(
        sum("amount").alias("total_sales")
    )
)


product_window = (
    Window
    .partitionBy("category")
    .orderBy(col("total_sales").desc())
)

# ------------------------------------------------------------
#  RANK PRODUCTS


top_products_df = (
    product_sales_df
    .withColumn(
        "row_num",
        row_number().over(product_window)
    )
    .filter(col("row_num") <= 2)
    .drop("row_num")
)

top_products_df.show()


# ============================================================
# PROBLEM 3 — CUSTOMER RUNNING REVENUE
# ============================================================

order_data = [
    (101, "2026-01-05", 1000),
    (101, "2026-01-10", 1500),
    (101, "2026-01-20", 2000),
    (101, "2026-02-01", 1200),

    (102, "2026-01-03", 500),
    (102, "2026-01-15", 700),
    (102, "2026-02-05", 1000),

    (103, "2026-01-07", 800),
    (103, "2026-01-25", 1200)
]

orders_df = spark.createDataFrame(
    order_data,
    ["customer_id", "order_date", "amount"]
)

spark.stop()