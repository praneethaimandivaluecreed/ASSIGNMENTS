import pandas as pd
import logging


logger = logging.getLogger(__name__)


# extracting from the data
def extract_data(file_path):

    logger.info(
        f"extraction_start | File: {file_path}"
    )

    try:
        df = pd.read_csv(file_path)

        logger.info(
            f"extraction_complete | "
            f"Records: {len(df)} | "
            f"Columns: {len(df.columns)}"
        )

        return df

    except Exception:
        logger.exception(
            f"extraction_failed | File: {file_path}"
        )
        raise