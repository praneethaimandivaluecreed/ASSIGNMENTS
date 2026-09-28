
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    DoubleType
)

from pyspark.sql.functions import (
    col,
    trim,
    lower,
    upper,
    initcap,
    regexp_replace,
    to_date
)


# 2. CREATE SPARK SESSION

spark = (
    SparkSession.builder
    .appName("EmployeeStandardization")
    .master("local[*]")
    .getOrCreate()
)


# FILE PATHS

HR_FILE = "employees_hr.csv"
PAYROLL_FILE = "employees_payroll.csv"

# DEFINE SOURCE SCHEMAS

hr_schema = StructType([
    StructField("employee_id", IntegerType(), True),
    StructField("employee_name", StringType(), True),
    StructField("department", StringType(), True),
    StructField("salary", DoubleType(), True),
    StructField("hire_date", StringType(), True),
    StructField("email", StringType(), True)
])


payroll_schema = StructType([
    StructField("emp_id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("dept", StringType(), True),
    StructField("monthly_salary", DoubleType(), True),
    StructField("joining_date", StringType(), True),
    StructField("work_email", StringType(), True)
])



#  READ RAW FILES

hr_raw = (
    spark.read
    .option("header", True)
    .schema(hr_schema)
    .csv(HR_FILE)
)

payroll_raw = (
    spark.read
    .option("header", True)
    .schema(payroll_schema)
    .csv(PAYROLL_FILE)
)



# INSPECT RAW DATA

hr_raw.show(truncate=False)
hr_raw.printSchema()

payroll_raw.show(truncate=False)
payroll_raw.printSchema()

# REUSABLE STANDARDIZATION FUNCTION

def standardize_employee_data(df, source):

    if source == "hr":

        result = df.select(
            col("employee_id").alias("employee_id"),

            initcap(
                trim(
                    regexp_replace(
                        col("employee_name"),
                        r"\s+",
                        " "
                    )
                )
            ).alias("employee_name"),

            upper(
                trim(col("department"))
            ).alias("department"),

            col("salary").alias("salary"),

            to_date(
                col("hire_date"),
                "yyyy-MM-dd"
            ).alias("hire_date"),

            lower(
                trim(col("email"))
            ).alias("email")
        )

    elif source == "payroll":

        result = df.select(
            col("emp_id").alias("employee_id"),

            initcap(
                trim(
                    regexp_replace(
                        col("name"),
                        r"\s+",
                        " "
                    )
                )
            ).alias("employee_name"),

            upper(
                trim(col("dept"))
            ).alias("department"),

            col("monthly_salary").alias("salary"),

            to_date(
                col("joining_date"),
                "dd-MM-yyyy"
            ).alias("hire_date"),

            lower(
                trim(col("work_email"))
            ).alias("email")
        )

    else:
        raise ValueError("Invalid source")

    return result

#  STANDARDIZE BOTH SOURCES

hr_clean = standardize_employee_data(
    hr_raw,
    "hr"
)

payroll_clean = standardize_employee_data(
    payroll_raw,
    "payroll"
)



# COMBINE THE DATA
employees = hr_clean.unionByName(payroll_clean)

# FINAL RESULT
employees.show(truncate=False)
employees.printSchema()

# BASIC VALIDATION

print("HR records:", hr_clean.count())
print("Payroll records:", payroll_clean.count())
print("Final records:", employees.count())

print("Final columns:", employees.columns)



# CHECK FOR NULLS

employees.filter(
    col("employee_id").isNull()
    | col("employee_name").isNull()
    | col("department").isNull()
    | col("salary").isNull()
    | col("hire_date").isNull()
    | col("email").isNull()
).show(truncate=False)