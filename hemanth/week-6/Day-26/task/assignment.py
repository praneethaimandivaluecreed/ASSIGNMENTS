from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField,
    IntegerType, StringType, DoubleType
)
from pyspark.sql.window import Window


# ============================================================
# 1. SPARK SESSION
# ============================================================

spark = (
    SparkSession.builder
    .appName("Day26_WindowFunctions")
    .master("local[*]")
    .getOrCreate()
)


# ============================================================
# 2. DATA + EXPLICIT SCHEMA
# ============================================================

orders_data = [
    (101, 1, "2026-01-05", 500.0),
    (102, 1, "2026-01-10", 700.0),
    (103, 1, "2026-01-15", 300.0),

    (104, 2, "2026-01-03", 400.0),
    (105, 2, "2026-01-12", 900.0),
    (106, 2, "2026-01-20", 600.0),

    (107, 3, "2026-01-08", 1000.0),
    (108, 3, "2026-01-18", 500.0),

    (109, 4, "2026-02-01", 250.0),
    (110, 4, "2026-02-05", 750.0),
    (111, 4, "2026-02-10", 750.0)
]

schema = StructType([
    StructField("order_id", IntegerType(), False),
    StructField("customer_id", IntegerType(), False),
    StructField("order_date", StringType(), False),
    StructField("amount", DoubleType(), False)
])

orders = spark.createDataFrame(orders_data, schema)

orders = orders.withColumn(
    "order_date",
    F.to_date("order_date")
)

orders.show()
orders.printSchema()


# ============================================================
# 3. WINDOW DEFINITIONS
# ============================================================

customer_date_window = (
    Window
    .partitionBy("customer_id")
    .orderBy("order_date", "order_id")
)

customer_amount_window = (
    Window
    .partitionBy("customer_id")
    .orderBy(F.col("amount").desc(), F.col("order_id"))
)


# ============================================================
# 4. PROBLEM 1 — LATEST ORDER PER CUSTOMER
# ============================================================

latest_orders = (
    orders
    .withColumn(
        "row_num",
        F.row_number().over(
            Window
            .partitionBy("customer_id")
            .orderBy(
                F.col("order_date").desc(),
                F.col("order_id").desc()
            )
        )
    )
    .filter(F.col("row_num") == 1)
    .drop("row_num")
    .orderBy("customer_id")
)

print("\n--- PROBLEM 1: LATEST ORDER ---")
latest_orders.show()

assert latest_orders.count() == 4


# ============================================================
# 5. PROBLEM 2 — TOP 2 ORDERS PER CUSTOMER
# ============================================================

top_2_orders = (
    orders
    .withColumn(
        "order_rank",
        F.row_number().over(customer_amount_window)
    )
    .filter(F.col("order_rank") <= 2)
    .orderBy("customer_id", "order_rank")
)

print("\n--- PROBLEM 2: TOP 2 ORDERS ---")
top_2_orders.show()

assert top_2_orders.filter(
    F.col("customer_id") == 1
).count() == 2


# ============================================================
# 6. PROBLEM 3 — RUNNING TOTAL PER CUSTOMER
# ============================================================

running_window = (
    Window
    .partitionBy("customer_id")
    .orderBy("order_date", "order_id")
    .rowsBetween(
        Window.unboundedPreceding,
        Window.currentRow
    )
)

running_total = (
    orders
    .withColumn(
        "running_total",
        F.sum("amount").over(running_window)
    )
    .orderBy("customer_id", "order_date")
)

print("\n--- PROBLEM 3: RUNNING TOTAL ---")
running_total.show()

customer_1_final = (
    running_total
    .filter(F.col("customer_id") == 1)
    .orderBy(F.col("order_date").desc())
    .first()
)

assert customer_1_final["running_total"] == 1500.0


# ============================================================
# 7. PROBLEM 4 — PREVIOUS ORDER + DIFFERENCE
# ============================================================

previous_window = (
    Window
    .partitionBy("customer_id")
    .orderBy("order_date", "order_id")
)

previous_order = (
    orders
    .withColumn(
        "previous_amount",
        F.lag("amount").over(previous_window)
    )
    .withColumn(
        "amount_difference",
        F.col("amount") - F.col("previous_amount")
    )
    .orderBy("customer_id", "order_date")
)

print("\n--- PROBLEM 4: PREVIOUS ORDER ---")
previous_order.show()

second_order_customer_1 = (
    previous_order
    .filter(
        (F.col("customer_id") == 1) &
        (F.col("order_id") == 102)
    )
    .first()
)

assert second_order_customer_1["previous_amount"] == 500.0
assert second_order_customer_1["amount_difference"] == 200.0


# ============================================================
# 8. PROBLEM 5 — TOP 2 CUSTOMERS PER MONTH
# ============================================================

monthly_spend = (
    orders
    .withColumn(
        "month",
        F.date_format("order_date", "yyyy-MM")
    )
    .groupBy("month", "customer_id")
    .agg(
        F.sum("amount").alias("total_spend")
    )
)

monthly_window = (
    Window
    .partitionBy("month")
    .orderBy(
        F.col("total_spend").desc(),
        F.col("customer_id")
    )
)

top_customers_monthly = (
    monthly_spend
    .withColumn(
        "customer_rank",
        F.row_number().over(monthly_window)
    )
    .filter(F.col("customer_rank") <= 2)
    .orderBy("month", "customer_rank")
)

print("\n--- PROBLEM 5: TOP 2 CUSTOMERS PER MONTH ---")
top_customers_monthly.show()

assert (
    top_customers_monthly
    .groupBy("month")
    .count()
    .filter(F.col("count") > 2)
    .count()
    == 0
)


# ============================================================
# 9. EXECUTION PLAN
# ============================================================

print("\n--- EXECUTION PLAN: RUNNING TOTAL ---")
running_total.explain("formatted")


print("\nAll Day-26 validations passed.")


# ============================================================
# 10. STOP SPARK
# ============================================================

spark.stop()