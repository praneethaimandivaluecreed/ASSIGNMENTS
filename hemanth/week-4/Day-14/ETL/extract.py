import json
import pandas as pd


class ExtractionError(Exception):
    pass


def extract_students(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        df = pd.DataFrame(data)

        if df.empty:
            raise ExtractionError("Extracted data is empty")

        return df

    except FileNotFoundError:
        raise ExtractionError(f"File not found: {filepath}")

    except json.JSONDecodeError:
        raise ExtractionError("Invalid JSON file")

    except Exception as e:
        raise ExtractionError(f"Extraction failed: {e}")