import json
import csv
import logging

# Logging setup
logging.basicConfig(
    filename="etl.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def extract():
    logger.info("Starting extraction")

    with open("data.json", "r") as file:
        data = json.load(file)

    logger.info("Extracted %d records", len(data))

    return data


def transform(data):
    logger.info("Starting transformation")

    transformed_data = []

    for record in data:
        transformed_data.append({
            "name": record["name"].upper(),
            "age": int(record["age"])
        })

    logger.info("Transformation completed")

    return transformed_data


def load(data):
    logger.info("Starting loading")

    with open("output.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["name", "age"]
        )

        writer.writeheader()
        writer.writerows(data)

    logger.info("Loaded %d records into CSV", len(data))


# ETL Pipeline
logger.info("ETL PIPELINE STARTED")

try:
    data = extract()
    data = transform(data)
    load(data)

    logger.info("ETL PIPELINE COMPLETED")

except Exception as e:
    logger.exception("ETL PIPELINE FAILED")