from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date


# creating spark session
spark = SparkSession.builder \
    .appName("Week5_Sales_Analytics") \
    .getOrCreate()

print("Spark Version:", spark.version)


# reading the csv file
df = spark.read.csv(
    "ASSIGNMENTS/praneetha/Week5/Day5/assignment/week5_sales.csv",
    header=True,
    inferSchema=True
)

print("\nRaw Data:")
df.show()

print("\nSchema:")
df.printSchema()

print("\nTotal Rows:", df.count())


# converting amount into double and order_date into date
clean_df = df.withColumn(
    "amount",
    col("amount").cast("double")
).withColumn(
    "order_date",
    to_date(col("order_date"))
)

print("\nCleaned Data:")
clean_df.show()

print("\nCleaned Schema:")
clean_df.printSchema()


# creating temporary view for using spark sql
clean_df.createOrReplaceTempView("sales")

print("\nSales Temporary View:")
spark.sql("""
    SELECT *
    FROM sales
""").show()


# finding orders where amount is greater than 10000
high_value_orders = spark.sql("""
    SELECT
        order_id,
        customer_name,
        product,
        amount
    FROM sales
    WHERE amount > 10000
    ORDER BY amount DESC
""")

print("\nOrders Above 10000:")
high_value_orders.show()


# calculating total sales for each department
department_sales = spark.sql("""
    SELECT
        department,
        SUM(amount) AS total_sales
    FROM sales
    GROUP BY department
    ORDER BY total_sales DESC
""")

print("\nDepartment Sales:")
department_sales.show()


# calculating total amount spent by each customer
customer_sales = spark.sql("""
    SELECT
        customer_id,
        customer_name,
        department,
        SUM(amount) AS total_spent
    FROM sales
    GROUP BY
        customer_id,
        customer_name,
        department
    ORDER BY total_spent DESC
""")

print("\nCustomer Sales:")
customer_sales.show()


# creating department data for join operation
department_data = [
    ("Electronics", "Electronic Products"),
    ("Furniture", "Home Furniture"),
    ("Clothing", "Fashion")
]

department_df = spark.createDataFrame(
    department_data,
    ["department", "department_description"]
)

print("\nDepartment Data:")
department_df.show()


# creating temporary view for department data
department_df.createOrReplaceTempView("departments")


# joining sales data with department data and calculating total sales
department_analysis = spark.sql("""
    SELECT
        s.department,
        d.department_description,
        SUM(s.amount) AS total_sales
    FROM sales s
    INNER JOIN departments d
        ON s.department = d.department
    GROUP BY
        s.department,
        d.department_description
    ORDER BY total_sales DESC
""")

print("\nDepartment Analysis:")
department_analysis.show()


# creating temporary view for customer sales
customer_sales.createOrReplaceTempView("customer_sales")


# ranking customers based on their total spending within each department
ranked_customers = spark.sql("""
    SELECT
        customer_id,
        customer_name,
        department,
        total_spent,
        RANK() OVER (
            PARTITION BY department
            ORDER BY total_spent DESC
        ) AS customer_rank
    FROM customer_sales
""")

print("\nCustomers Ranked By Department:")
ranked_customers.show()


# creating temporary view for ranked customers
ranked_customers.createOrReplaceTempView("ranked_customers")


# finding the highest spending customer in each department
top_customers = spark.sql("""
    SELECT
        customer_id,
        customer_name,
        department,
        total_spent,
        customer_rank
    FROM ranked_customers
    WHERE customer_rank = 1
    ORDER BY department
""")

print("\nTop Customer In Each Department:")
top_customers.show()


# displaying the execution plan
print("\nExecution Plan:")
ranked_customers.explain("formatted")


# stopping spark session
spark.stop()