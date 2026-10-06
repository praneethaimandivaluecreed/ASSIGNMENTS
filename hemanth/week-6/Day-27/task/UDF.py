from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import (
    StructType, StructField,
    IntegerType, StringType, DoubleType
)


# ============================================================
# 1. SPARK SESSION
# ============================================================

spark = (
    SparkSession.builder
    .appName("Day27_ReusableTransformations")
    .master("local[*]")
    .getOrCreate()
)


# ============================================================
# 2. INPUT DATA + EXPLICIT SCHEMA
# ============================================================

customer_data = [
    (1, "  alice johnson  ", " ALICE@EXAMPLE.COM ", 75000.0, "VIP-1001"),
    (2, "bob smith", " Bob@Example.com", 45000.0, "EMP-2001"),
    (3, "  CHARLIE BROWN", "charlie@example.com  ", 120000.0, "CUS-3001"),
    (4, "david lee ", " DAVID@EXAMPLE.COM ", 55000.0, "CUS-3002"),
    (5, None, None, None, None)
]

schema = StructType([
    StructField("customer_id", IntegerType(), False),
    StructField("name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("salary", DoubleType(), True),
    StructField("customer_code", StringType(), True)
])

df = spark.createDataFrame(customer_data, schema)


# ============================================================
# 3. REUSABLE TRANSFORMATION FUNCTIONS
# ============================================================

def clean_names(df):
    return df.withColumn(
        "clean_name",
        F.initcap(F.trim(F.col("name")))
    )


def clean_emails(df):
    return df.withColumn(
        "clean_email",
        F.lower(F.trim(F.col("email")))
    )


def create_salary_band(df):
    return df.withColumn(
        "salary_band",
        F.when(F.col("salary").isNull(), "UNKNOWN")
         .when(F.col("salary") >= 100000, "HIGH")
         .when(F.col("salary") >= 50000, "MEDIUM")
         .otherwise("LOW")
    )


def classify_customer(df):
    return df.withColumn(
        "customer_type",
        F.when(F.col("customer_code").isNull(), "UNKNOWN")
         .when(F.col("customer_code").startswith("VIP-"), "VIP")
         .when(F.col("customer_code").startswith("EMP-"), "EMPLOYEE")
         .otherwise("CUSTOMER")
    )


# ============================================================
# 4. GENUINELY CUSTOM BUSINESS LOGIC
# ============================================================

def custom_segment_logic(salary, customer_type):
    if salary is None or customer_type is None:
        return "UNKNOWN"

    if customer_type == "VIP" and salary >= 70000:
        return "PREMIUM_VIP"

    if customer_type == "EMPLOYEE":
        return "INTERNAL"

    if salary >= 100000:
        return "HIGH_VALUE"

    return "STANDARD"


custom_segment_udf = F.udf(
    custom_segment_logic,
    StringType()
)


def create_custom_segment(df):
    return df.withColumn(
        "custom_segment",
        custom_segment_udf(
            F.col("salary"),
            F.col("customer_type")
        )
    )


# ============================================================
# 5. PIPELINE USING .transform()
# ============================================================

result = (
    df
    .transform(clean_names)
    .transform(clean_emails)
    .transform(create_salary_band)
    .transform(classify_customer)
    .transform(create_custom_segment)
)


# ============================================================
# 6. DISPLAY RESULT
# ============================================================

print("\n--- FINAL TRANSFORMED DATA ---")

result.select(
    "customer_id",
    "clean_name",
    "clean_email",
    "salary",
    "customer_code",
    "salary_band",
    "customer_type",
    "custom_segment"
).show(truncate=False)


# ============================================================
# 7. SCHEMA
# ============================================================

print("\n--- SCHEMA ---")
result.printSchema()


# ============================================================
# 8. VALIDATION
# ============================================================

assert result.count() == 5

alice = (
    result
    .filter(F.col("customer_id") == 1)
    .first()
)

assert alice["clean_name"] == "Alice Johnson"
assert alice["clean_email"] == "alice@example.com"
assert alice["salary_band"] == "MEDIUM"
assert alice["customer_type"] == "VIP"
assert alice["custom_segment"] == "PREMIUM_VIP"


charlie = (
    result
    .filter(F.col("customer_id") == 3)
    .first()
)

assert charlie["salary_band"] == "HIGH"
assert charlie["customer_type"] == "CUSTOMER"
assert charlie["custom_segment"] == "HIGH_VALUE"


null_customer = (
    result
    .filter(F.col("customer_id") == 5)
    .first()
)

assert null_customer["salary_band"] == "UNKNOWN"
assert null_customer["customer_type"] == "UNKNOWN"
assert null_customer["custom_segment"] == "UNKNOWN"

print("\nAll validations passed.")


# ============================================================
# 9. EXECUTION PLAN
# ============================================================

print("\n--- EXECUTION PLAN ---")
result.explain("formatted")


# ============================================================
# 10. STOP SPARK
# ============================================================

spark.stop()