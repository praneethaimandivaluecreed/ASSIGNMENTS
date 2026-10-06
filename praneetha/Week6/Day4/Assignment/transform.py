# with reusable functions and without udfs

from pyspark.sql import SparkSession
from pyspark.sql.functions import (col, lower, trim, when, split)

# creating spark session
spark = (SparkSession.builder
         .appName("transformation_pipeline")
         .master("local[*]")
         .getOrCreate()
         )

# data
data = [
    (101, " JOHN ", "JOHN@GMAIL.COM", 75000),
    (102, " Mary ", "mary@yahoo.com", 55000),
    (103, " TOM ", "tom@company.com", 120000),
    (104, " Lisa ", None, 65000),
    (105, " Bob ", "bob@gmail.com", -5000)
]
columns = [
    "employee_id",
    "name",
    "email",
    "salary"
]

#creating spark dataframe
df = spark.createDataFrame(data, columns)

# printing raw data
print("Raw data :")
df.show()


# fxn that standadizes the data
def standardize_data(df):
    return df.withColumn("name", lower(trim(col('name')))).withColumn("email", lower(trim(col('email'))))

# fxn to validate data
def validate_data(df):
    return(
        df.filter((col('employee_id').isNotNull()) &
                  (col('salary') > 0)) 
    )

# fxn to create salary category column
def create_salary_category(df):
    return(
        df.withColumn("sal_category", when(col('salary') >= 100000, "High")
                      .when(col('salary') >= 60000, "Medium")
                      .otherwise("low")
                      )
    )

#fxn to add email domain
def add_email_domain(df):

    return df.withColumn(
        "email_domain",
        split(col("email"), "@").getItem(1)
    )


# complete pipeline
df = (df.transform(standardize_data)
      .transform(validate_data)
      .transform(create_salary_category)
      .transform(add_email_domain))

# displaying data after transformations & validations
print("Final Data : ")
df.show()

# stopping spark sessiom
spark.stop()


# without reusable functions with udf
# from pyspark.sql import SparkSession
# from pyspark.sql.functions import (
#     col,
#     lower,
#     trim,
#     when,
#     udf
# )
# from pyspark.sql.types import StringType

# spark = (
#     SparkSession.builder
#     .appName("Employee_UDF")
#     .master("local[*]")
#     .getOrCreate()
# )


# data = [
#     (101, " JOHN ", "JOHN@GMAIL.COM", 75000),
#     (102, " Mary ", "mary@yahoo.com", 55000),
#     (103, " TOM ", "tom@company.com", 120000),
#     (104, " Lisa ", None, 65000),
#     (105, " Bob ", "bob@gmail.com", -5000)
# ]

# columns = [
#     "employee_id",
#     "name",
#     "email",
#     "salary"
# ]

# df = spark.createDataFrame(data, columns)

# def get_email_domain(email):

#     if email is None:
#         return None

#     return email.split("@")[1]


# email_domain_udf = udf(
#     get_email_domain,
#     StringType()
# )

# df = (
#     df

#     # Standardize name
#     .withColumn(
#         "name",
#         lower(trim(col("name")))
#     )

#     # Standardize email
#     .withColumn(
#         "email",
#         lower(trim(col("email")))
#     )

#     # Validate data
#     .filter(
#         (col("employee_id").isNotNull()) &
#         (col("salary") > 0)
#     )

#     # Salary band
#     .withColumn(
#         "salary_band",
#         when(col("salary") >= 100000, "High")
#         .when(col("salary") >= 60000, "Medium")
#         .otherwise("Low")
#     )

#     # Email domain using UDF
#     .withColumn(
#         "email_domain",
#         email_domain_udf(col("email"))
#     )
# )

# df.show()

# spark.stop()