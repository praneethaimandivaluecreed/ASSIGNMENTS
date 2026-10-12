import pyodbc

from config import(
    DB_SERVER,
    DB_DATABASE,
    DB_USERNAME,
    DB_PASSWORD,
    DB_DRIVER
)

def load(data):
    print("Starting load...")

    connection_string=(
        f"DRIVER={DB_DRIVER};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_USERNAME};"
        f"PWD={DB_PASSWORD};"
        f"TrustServerCertificate=yes;"
    )

    connection=pyodbc.connect(connection_string)

    cursor=connection.cursor()

    cursor.execute("""
IF OBJECT_ID('ProductsETL' , 'U') is NULL  # U defines user defined tables
BEGIN 
 CREATE TABLE ProductsETL(product_id INT , product_name VARCHAR(100) , price FLOAT , category VARCHAR(100)) END
""")

    for _, row in data.iterrows():   # gives rows 

        cursor.execute("""
            INSERT INTO ProductsETL
            (product_id, product_name, price, category)
            VALUES (?, ?, ?, ?)
        """,
        int(row["product_id"]),
        row["product_name"],
        float(row["price"]),
        row["category"])


    for row in data:  #it returns column names 
        print(row)

    connection.commit()

    cursor.close()
    connection.close()

    print(f"Loaded {len(data)} records.")


