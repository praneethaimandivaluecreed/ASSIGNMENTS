from extract import extract_students, ExtractionError
from transform import transform_products, TransformationError
from validate import validate_students
from load import load_df, LoadError
from logger import logger


def main():

    filepath = "messy_student_records.json"

    # ---------------- PIPELINE START ----------------
    logger.info("ETL pipeline started")

    # ---------------- EXTRACTION ----------------
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

    # ---------------- TRANSFORMATION ----------------
    try:
        logger.info("Transformation started")

        duplicate_count = extracted_df.duplicated().sum()

        logger.info(
            f"Duplicate records found: {duplicate_count}"
        )

        transformed_df = transform_products(extracted_df)

        logger.info(
            f"Transformation completed: {len(transformed_df)} records"
        )

    except TransformationError as e:
        logger.error(f"Transformation failed: {e}")
        logger.error("ETL pipeline failed during transformation")
        return

    # ---------------- VALIDATION ----------------
    try:
        logger.info("Validation started")

        valid_df, invalid_df = validate_students(transformed_df)

        logger.info(
            f"Validation completed: {len(valid_df)} valid records"
        )

        logger.warning(
            f"Invalid records found: {len(invalid_df)}"
        )

        # Save invalid records for investigation
        if not invalid_df.empty:
            invalid_df.to_csv(
                "invalid_student_records.csv",
                index=False
            )

            logger.warning(
                "Invalid records saved to invalid_student_records.csv"
            )

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        logger.error("ETL pipeline failed during validation")
        return

    # ---------------- LOADING ----------------
    try:
        load_df(valid_df)

        logger.info(
            f"Loading completed: {len(valid_df)} records"
        )

    except LoadError as e:
        logger.error(f"Loading failed: {e}")
        logger.error("ETL pipeline failed during loading")
        return

    # ---------------- PIPELINE END ----------------
    logger.info("ETL pipeline completed successfully")
    logger.info("ETL pipeline ended")


if __name__ == "__main__":
    main()