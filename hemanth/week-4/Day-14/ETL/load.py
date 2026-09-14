from config import connection_string
import pyodbc


class LoadError(Exception):
    pass


def load_df(df):

    connection = None

    try:
        # Connect to SQL Server
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        print("Connection successful")

        # Create table if it does not exist
        create_table_query = """
        IF OBJECT_ID('Students', 'U') IS NULL
        BEGIN
            CREATE TABLE Students (
                student_id INT,
                student_name VARCHAR(100),
                age INT,
                gender VARCHAR(20),
                course VARCHAR(50),
                marks DECIMAL(5,2),
                attendance DECIMAL(5,2),
                city VARCHAR(50)
            )
        END
        """

        cursor.execute(create_table_query)
        connection.commit()

        print("Table checked/created successfully")

        # Parameterized insert query
        insert_query = """
        INSERT INTO Students
        (
            student_id,
            student_name,
            age,
            gender,
            course,
            marks,
            attendance,
            city
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Convert DataFrame into tuples
        records = list(df.itertuples(index=False, name=None))

        # Load data in batches of 10
        batch_size = 10

        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]

            cursor.executemany(insert_query, batch)
            connection.commit()

            print(f"Batch {(i // batch_size) + 1} loaded: {len(batch)} records")

        print("All data loaded successfully")

    except pyodbc.Error as e:

        # Rollback failed database operation
        if connection:
            connection.rollback()

        raise LoadError(f"Loading failed: {e}")

    finally:

        # Always close the connection
        if connection:
            connection.close()

        print("Connection closed")