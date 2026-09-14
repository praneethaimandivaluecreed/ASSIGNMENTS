# here we finally load the transformed data into our database
# we use batch loading and transaction handling

import os
import pyodbc
from dotenv import load_dotenv
import pandas as pd


# calling load_dotenv
load_dotenv()


# custom exception for loading failures
class ETLLoadError(Exception):
    pass


# connecting with SQL Server
def get_connection():

    try:

        connection_string = (
            f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_DATABASE')};"
            f"Trusted_Connection={os.getenv('DB_TRUSTED_CONNECTION')};"
            f"TrustServerCertificate={os.getenv('DB_TRUST_SERVER_CERTIFICATE')};"
        )

        return pyodbc.connect(connection_string)

    except pyodbc.Error as e:

        raise ETLLoadError(
            f"Database connection failed: {e}"
        ) from e


# creating the ETL_Sales table
def create_table(connection):

    cursor = connection.cursor()

    try:

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

        print("Table checked/created successfully.")

    except pyodbc.Error as e:

        connection.rollback()

        raise ETLLoadError(
            f"Table creation failed: {e}"
        ) from e

    finally:

        cursor.close()


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

    try:

        # Convert Pandas NaN/NaT values to Python None
        # so SQL Server can store them as NULL
        df = df.astype(object).where(
            pd.notna(df),
            None
        )

        data = list(
            df.itertuples(
                index=False,
                name=None
            )
        )

        # Batch loading
        for start in range(
            0,
            len(data),
            batch_size
        ):

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

        # Commit only after ALL batches succeed
        connection.commit()

        print("All batches loaded successfully.")
        print("Transaction committed.")

    except (pyodbc.Error, ValueError, TypeError) as e:

        # Undo all inserts if any batch fails
        connection.rollback()

        print("Loading failed.")
        print("Transaction rolled back.")

        raise ETLLoadError(
            f"Data loading failed: {e}"
        ) from e

    except Exception as e:

        connection.rollback()

        print("Unexpected loading failure.")
        print("Transaction rolled back.")

        raise ETLLoadError(
            f"Unexpected loading error: {e}"
        ) from e

    finally:

        cursor.close()


# calling the functions
if __name__ == "__main__":

    from extract import extract_data
    from transform import transform_data
    from validate import validate_data

    print("Starting ETL load test...")

    connection = None

    try:

        # -----------------------------
        # Extract
        # -----------------------------

        customers, orders, payments = extract_data()

        # -----------------------------
        # Transform
        # -----------------------------

        transformed_data = transform_data(
            customers,
            orders,
            payments
        )

        # -----------------------------
        # Validate
        # -----------------------------

        validate_data(transformed_data)

        # -----------------------------
        # Load
        # -----------------------------

        connection = get_connection()

        print("Connected to SQL Server.")

        create_table(connection)

        load_data(
            connection,
            transformed_data,
            batch_size=500
        )

        print("\nETL load completed successfully.")

    except ETLLoadError as e:

        print("\nETL Load Error:")
        print(e)

    except Exception as e:

        print("\nUnexpected pipeline error:")
        print(e)

    finally:

        if connection:

            connection.close()

            print("Database connection closed.")