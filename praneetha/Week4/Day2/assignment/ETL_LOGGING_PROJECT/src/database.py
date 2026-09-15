import os
import pyodbc
import logging
from dotenv import load_dotenv


logger = logging.getLogger(__name__)

load_dotenv()

# connecting to db
def get_connection():

    logger.info(
        "database_connection_start"
    )

    try:

        connection_string = (
            f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_DATABASE')};"
            f"Trusted_Connection={os.getenv('DB_TRUSTED_CONNECTION')};"
            f"TrustServerCertificate={os.getenv('DB_TRUST_SERVER_CERTIFICATE')};"
        )

        connection = pyodbc.connect(
            connection_string
        )

        logger.info(
            "database_connection_success"
        )

        return connection

    except Exception:
        logger.exception(
            "database_connection_failed"
        )
        raise