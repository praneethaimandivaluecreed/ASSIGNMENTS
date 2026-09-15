from extract import extract_students, ExtractionError
from transform import transform_products, TransformationError
from load import load_df, LoadError
from logger import logger

def main():

    filepath = "messy_student_records.json"
    logger.info("ETL pipeline started")
    try:
        logger.info(f"Extracting student records from {filepath}")

        extracted_df = extract_students(filepath)

        logger.info(
            f"Extraction completed: {len(extracted_df)} records"
        )

    except ExtractionError as e:
        logger.error(f"Extraction failed: {e}")
        logger.error("ETL pipeline failed during extraction")
        return
    
    try:
        logger.info("Transformation started")

        # Count duplicates before removing them
        duplicate_count = extracted_df.duplicated().sum()
        logger.info(f"Duplicate records found: {duplicate_count}")

        transformed_df = transform_products(extracted_df)

        # Count final valid records
        logger.info(
            f"Transformation completed: {len(transformed_df)} valid records"
        )

    except TransformationError as e:
        logger.error(f"Transformation failed: {e}")
        logger.error("ETL pipeline failed during transformation")
        return

    try:
        load_df(transformed_df)

        logger.info(
            f"Loading completed: {len(transformed_df)} records"
        )

    except LoadError as e:
        logger.error(f"Loading failed: {e}")
        logger.error("ETL pipeline failed during loading")
        return

    logger.info("ETL pipeline completed successfully")
    logger.info("ETL pipeline ended")


if __name__ == "__main__":
    main()