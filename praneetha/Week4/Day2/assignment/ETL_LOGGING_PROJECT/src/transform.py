import pandas as pd
import logging


logger = logging.getLogger(__name__)

# fxn to transform the data
def transform_data(df):

    logger.info(
        f"transformation_start | Records: {len(df)}"
    )

    try:

        df = df.copy()

        # Remove duplicate OrderIDs
        before = len(df)

        df = df.drop_duplicates(
            subset=["OrderID"],
            keep="first"
        )

        duplicates_removed = before - len(df)

        logger.info(
            f"duplicates_removed | Count: {duplicates_removed}"
        )

        # Fill missing CustomerName
        df["CustomerName"] = df["CustomerName"].fillna("Unknown")

        # Fill missing City
        df["City"] = df["City"].fillna("Unknown")

        # Fill missing Product
        df["Product"] = df["Product"].fillna("Unknown")

        # Fix invalid Age
        df.loc[
            (df["Age"] < 18) | (df["Age"] > 100),
            "Age"
        ] = None

        df["Age"] = df["Age"].fillna(
            df["Age"].median()
        )

        # Fix invalid Quantity
        df.loc[
            df["Quantity"] <= 0,
            "Quantity"
        ] = 1

        # Fix negative Amount
        df.loc[
            df["Amount"] < 0,
            "Amount"
        ] = None

        df["Amount"] = df["Amount"].fillna(
            df["Amount"].median()
        )

        # Fill missing PaymentMethod
        df["PaymentMethod"] = df["PaymentMethod"].fillna(
            "Unknown"
        )

        # Convert OrderDate
        df["OrderDate"] = pd.to_datetime(
            df["OrderDate"]
        )

        # Create OrderMonth
        df["OrderMonth"] = df["OrderDate"].dt.month

        # Create OrderYear
        df["OrderYear"] = df["OrderDate"].dt.year

        # Calculate TotalAmount
        df["TotalAmount"] = (
            df["Quantity"] * df["Amount"]
        )

        logger.info(
            f"transformation_complete | "
            f"Records: {len(df)} | "
            f"Columns: {len(df.columns)}"
        )

        return df

    except Exception:
        logger.exception(
            "transformation_failed"
        )
        raise