import json
import pandas as pd
from logger import logger

class ExtractionError(Exception):
    pass

def extract_students(filepath):
    try:
        logger.info(f"Extraction started: file={filepath}")

        # Read JSON file
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Convert JSON data into DataFrame
        df = pd.DataFrame(data)

        # Check whether extracted data is empty
        if df.empty:
            raise ExtractionError("Extracted data is empty")

        logger.info(f"Extraction completed : records={len(df)}")

        return df

    except FileNotFoundError:
        logger.error(f"Extraction failed : file not found={filepath}")
        raise ExtractionError(f"File not found: {filepath}")

    except json.JSONDecodeError:
        logger.error("Extraction failed : invalid JSON")
        raise ExtractionError("Invalid JSON file")

    except ExtractionError:
        raise

    except Exception as e:
        logger.error(f"Extraction failed - error={e}")
        raise ExtractionError(f"Extraction failed: {e}")