import logging
import os

from src.logging_config import setup_logging
from src.extract import extract_data
from src.transform import transform_data

from src.database import get_connection
from src.load import load_data


logger = logging.getLogger(__name__)

# complete etl pipeline
def run_pipeline():

    logger.info(
        "pipeline_start | ETL pipeline started"
    )

    connection = None

    try:

        # -------------------------
        # EXTRACT
        # -------------------------

        source_file = "data/source/sales_data.csv"

        df = extract_data(source_file)

        # -------------------------
        # SAVE RAW DATA
        # -------------------------

        os.makedirs(
            "data/raw",
            exist_ok=True
        )

        raw_file = "data/raw/sales_data_raw.csv"

        df.to_csv(
            raw_file,
            index=False
        )

        logger.info(
            f"raw_data_saved | File: {raw_file}"
        )

        # -------------------------
        # TRANSFORM
        # -------------------------

        df = transform_data(df)

        # -------------------------
        # SAVE PROCESSED DATA
        # -------------------------

        os.makedirs(
            "data/processed",
            exist_ok=True
        )

        processed_file = (
            "data/processed/sales_data_processed.csv"
        )

        df.to_csv(
            processed_file,
            index=False
        )

        logger.info(
            f"processed_data_saved | "
            f"File: {processed_file}"
        )

        # -------------------------
        # DATABASE CONNECTION
        # -------------------------

        connection = get_connection()

        # -------------------------
        # LOAD
        # -------------------------

        load_data(
            df,
            connection
        )

        logger.info(
            f"pipeline_end | "
            f"Pipeline completed successfully | "
            f"Records: {len(df)}"
        )

    except Exception:

        logger.exception(
            "pipeline_failed | ETL pipeline failed"
        )

        raise

    finally:

        if connection:

            connection.close()

            logger.info(
                "database_connection_closed"
            )


if __name__ == "__main__":

    setup_logging()

    run_pipeline()