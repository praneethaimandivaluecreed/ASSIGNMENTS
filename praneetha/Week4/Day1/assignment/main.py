# main.py
# This file controls the complete ETL pipeline.
# It connects Extract → Transform → Validate → Load.

from extract import extract_data, ETLExtractionError
from transform import transform_data, ETLTransformationError
from validate import validate_data, ETLValidationError
from load import (
    get_connection,
    create_table,
    load_data,
    ETLLoadError
)


def run_pipeline():

    print("========== ETL PIPELINE STARTED ==========\n")

    # --------------------------------
    # 1. EXTRACT
    # --------------------------------

    try:

        print("Starting extraction...")

        customers, orders, payments = extract_data()

        print("Extraction completed successfully.\n")

    except ETLExtractionError as e:

        print("EXTRACTION FAILED")
        print(e)

        return


    # --------------------------------
    # 2. TRANSFORM
    # --------------------------------

    try:

        print("Starting transformation...")

        transformed_data = transform_data(
            customers,
            orders,
            payments
        )

        print("Transformation completed successfully.\n")

    except ETLTransformationError as e:

        print("TRANSFORMATION FAILED")
        print(e)

        return


    # --------------------------------
    # 3. VALIDATE
    # --------------------------------

    try:

        print("Starting validation...")

        validate_data(transformed_data)

        print("Validation completed successfully.\n")

    except ETLValidationError as e:

        print("VALIDATION FAILED")
        print(e)

        return


    # --------------------------------
    # 4. LOAD
    # --------------------------------

    connection = None

    try:

        print("Starting database loading...")

        connection = get_connection()

        print("Connected to SQL Server.")

        create_table(connection)

        load_data(
            connection,
            transformed_data,
            batch_size=500
        )

        print("\nLoading completed successfully.")

    except ETLLoadError as e:

        print("LOADING FAILED")
        print(e)

        return

    finally:

        if connection:

            connection.close()

            print("Database connection closed.")


    print("\n========== ETL PIPELINE COMPLETED ==========")


# Run the pipeline
if __name__ == "__main__":

    run_pipeline()