import logging
import os


# fxn to set up the logging object
def setup_logging():

    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/etl_pipeline.log"),
            logging.StreamHandler()
        ]
    )