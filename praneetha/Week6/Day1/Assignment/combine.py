# IMPORTS
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower,to_date
from pyspark.sql.types import(
    StructType,
    StructField,
    IntegerType,
    StringType,
    DateType
)

# creating spark session
spark = (
    SparkSession.builder
    .appName("Customer_Ingestion_Standardization")
    .master("local[*]")
    .getOrCreate()
)

# defining explicit schema of file a 
schema = StructType([
    StructField("customer_id", IntegerType(), True),
     StructField("name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("signup_date", DateType(), True)
])

# defining explicit schema of file b
schema_b = StructType([
    StructField("cust_id", IntegerType(), True),
    StructField("customer_name", StringType(), True),
    StructField("email_address", StringType(), True),
    StructField("registration_date", StringType(), True)
])


# ingestion fxn
def ingest_csv(path, schema):
    df = spark.read.csv(
        path,
        header = True,
        schema= schema
    )
    return df


# ingesting customer_file a & printing
df_a = ingest_csv(
    r"c:\Users\VC_User6.DESKTOP-22FFUC4\Desktop\DATA ANALYTICS\ASSIGNMENTS\praneetha\Week6\Day1\Assignment\customers_a.csv",
    schema
)

print("Customer A :")
df_a.show()


# ingesting customer_file b & printing
df_b = ingest_csv(
    r"c:\Users\VC_User6.DESKTOP-22FFUC4\Desktop\DATA ANALYTICS\ASSIGNMENTS\praneetha\Week6\Day1\Assignment\customers_b.csv",
    schema_b
)

print("Customer B")
df_b.show()


# standardize customer file A
def standardize_customer_a(df):

    return (
        df
        .select(
            col("customer_id"),
            trim(col("name")).alias("name"),
            lower(trim(col("email"))).alias("email"),
            col("signup_date")
        )
    )


# standardizing customer file B
def standardize_customer_b(df):

    return (
        df
        .select(
            col("cust_id").alias("customer_id"),
            trim(col("customer_name")).alias("name"),
            lower(trim(col("email_address"))).alias("email"),
            to_date(
                col("registration_date"),
                "yyyy-MM-dd"
            ).alias("signup_date")
        )
    )


# applying standardizations
standard_a = standardize_customer_a(df_a)
standard_b = standardize_customer_b(df_b)

# prinitng standardized data
print("Standardized Customer A:")
standard_a.show()

print("Standardized Customer B:")
standard_b.show()

# combining both datasets
final_df = standard_a.unionByName(standard_b)

# printing combined customer data
print("Final data :")
final_df.show()
print("Final schema")
final_df.printSchema()


# stopping spark session
spark.stop()