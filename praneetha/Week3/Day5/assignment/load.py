# here we finally load the transformed data into our db
# we will try to use batch loading the data

import os
import pyodbc
from dotenv import load_dotenv
import pandas as pd

# calling load_dotenv
load_dotenv()

# connecting with the ssms
def get_connection():

    connection_string = (
        f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_DATABASE')};"
        f"Trusted_Connection={os.getenv('DB_TRUSTED_CONNECTION')};"
        f"TrustServerCertificate={os.getenv('DB_TRUST_SERVER_CERTIFICATE')};"
    )

    # creating a connection string
    return pyodbc.connect(connection_string)



# creating 3 diff tables for orders, customers and payments
def create_table(connection):

    # create cursor using the connection
    cursor = connection.cursor()

    cursor.execute("""
        IF OBJECT_ID('ETL_Sales', 'U') IS NULL
        BEGIN

            CREATE TABLE ETL_Sales (

                OrderID INT,
                CustomerID INT,
                OrderDate DATE,
                Product VARCHAR(100),
                Quantity INT,
                Amount DECIMAL(12,2),

                Name VARCHAR(100),
                Age INT,
                City VARCHAR(100),
                Email VARCHAR(150),

                PaymentID INT,
                PaymentMethod VARCHAR(50),
                PaymentDate DATE,
                PaymentStatus VARCHAR(50),

                OrderMonth INT,
                OrderYear INT,
                TotalAmount DECIMAL(14,2)

            )

        END
    """)

    connection.commit()

    cursor.close()

    print("Table checked/created successfully.")


 # batch loading the data
def load_data(connection, df, batch_size=500):

    cursor = connection.cursor()

    insert_query = """
        INSERT INTO ETL_Sales (
            OrderID,
            CustomerID,
            OrderDate,
            Product,
            Quantity,
            Amount,
            Name,
            Age,
            City,
            Email,
            PaymentID,
            PaymentMethod,
            PaymentDate,
            PaymentStatus,
            OrderMonth,
            OrderYear,
            TotalAmount
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

   

    df = df.astype(object).where(pd.notna(df), None)

    data = list(
        df.itertuples(index=False, name=None)
    )
    try:

        for start in range(0, len(data), batch_size):

            batch = data[
                start:start + batch_size
            ]

            cursor.executemany(
                insert_query,
                batch
            )

            print(
                f"Loaded batch: "
                f"{start + 1} - "
                f"{start + len(batch)}"
            )

        connection.commit()

        print("All batches loaded successfully.")
        print("Transaction committed.")

    except Exception as e:

        connection.rollback()

        print("Loading failed.")
        print("Transaction rolled back.")
        print("Error:", e)

        raise

    finally:

        cursor.close()


# calling the fxn
if __name__ == "__main__":

    from extract import extract_data
    from transform import transform_data
    from validate import validate_data

    print("Starting ETL load test...")

    # Extract
    customers, orders, payments = extract_data()

    # Transform
    transformed_data = transform_data(
        customers,
        orders,
        payments
    )

    # Validate
    if not validate_data(transformed_data):

        print("Validation failed.")
        print("Data will not be loaded.")

    else:

        connection = None

        try:

            connection = get_connection()

            print("Connected to SQL Server.")

            create_table(connection)

            load_data(
                connection,
                transformed_data,
                batch_size=500
            )

        except Exception as e:

            print("Pipeline load failed:")
            print(e)

        finally:

            if connection:
                connection.close()

                print(
                    "Database connection closed."
                )