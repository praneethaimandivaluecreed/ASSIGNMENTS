
import pyodbc


# ===================== DATABASE CONNECTION =====================

connection = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=tcp:NICKYSLAP,1433;'
    'DATABASE=DataAnalytics;'
    'UID=colab_user;'
    'PWD=123456;'
    'TrustServerCertificate=yes;'
)

print("Connected successfully!")


# ===================== CURSOR =====================

cursor = connection.cursor()


try:

    # ===================== GET ALL DATA =====================

    cursor.execute("SELECT * FROM products")

    # Get all rows from products
    rows = cursor.fetchall()

    print("Total rows:", len(rows))


    # ===================== BATCH INSERT =====================

    batch_size = 7

    for i in range(0, len(rows), batch_size):

        # Create one batch of 5 rows
        batch = rows[i:i + batch_size]

        print("Loading batch:", i // batch_size + 1)
        print("Number of rows:", len(batch))


        # Insert the batch into product1
        cursor.executemany(
            """
            INSERT INTO product1
            (
                product_id,
                product_name,
                product_price,
                product_category,
                description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            batch
        )


        # Save the batch
        connection.commit()

        print("Batch loaded successfully!")


    print("All data loaded successfully!")


except pyodbc.Error as error:

    # Undo uncommitted changes if something fails
    connection.rollback()

    print("Error while loading data:")
    print(error)


finally:

    # ===================== CLOSE RESOURCES =====================

    cursor.close()
    connection.close()

    print("Connection closed.")

