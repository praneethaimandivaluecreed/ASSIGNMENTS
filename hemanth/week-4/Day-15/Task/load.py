from config import connection_string
import pyodbc
from logger import logger

class LoadError(Exception):
    pass

def load_df(df):

    connection = None

    try:
        logger.info(f"Loading started: {len(df)} records")

        # Connect to SQL Server
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        logger.info("Database connection successful")

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

        logger.info("Students table checked/created")

        # Insert query
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

        # Define batch size
        batch_size = 20

        total_batches = (len(records) + batch_size - 1) // batch_size

        # Load records batch by batch
        for i in range(0, len(records), batch_size):

            batch = records[i:i + batch_size]

            batch_number = (i // batch_size) + 1

            logger.info(
                f"Loading batch {batch_number}/{total_batches}: "
                f"{len(batch)} records"
            )

            cursor.executemany(insert_query, batch)
            connection.commit()

        logger.info(f"Loading completed: {len(records)} records")

    except pyodbc.Error as e:

        if connection:
            connection.rollback()

        logger.error(f"Loading failed: {e}")

        raise LoadError(f"Loading failed: {e}")

    finally:

        if connection:
            connection.close()
            logger.info("Database connection closed")