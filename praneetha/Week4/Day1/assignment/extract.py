# extraction part of our pipeline
# here we are extracting data from different sources

import pandas as pd


# custom exception for extraction failures
class ETLExtractionError(Exception):
    pass


# function to extract the data from the files
def extract_data():

    try:
        customers = pd.read_csv("data/customers.csv")
        orders = pd.read_csv("data/orders.csv")
        payments = pd.read_json("data/payments.json")

        # defensive check: make sure required columns exist
        required_customer_columns = {
            "CustomerID", "Name", "Age", "City", "Email"
        }

        required_order_columns = {
            "OrderID", "CustomerID", "OrderDate",
            "Product", "Quantity", "Amount"
        }

        required_payment_columns = {
            "PaymentID", "OrderID", "PaymentMethod",
            "PaymentDate", "PaymentStatus"
        }

        if not required_customer_columns.issubset(customers.columns):
            raise ValueError("Customers file is missing required columns.")

        if not required_order_columns.issubset(orders.columns):
            raise ValueError("Orders file is missing required columns.")

        if not required_payment_columns.issubset(payments.columns):
            raise ValueError("Payments file is missing required columns.")

        return customers, orders, payments

    except FileNotFoundError as e:
        raise ETLExtractionError(
            f"Extraction failed: source file not found - {e}"
        ) from e

    except pd.errors.EmptyDataError as e:
        raise ETLExtractionError(
            "Extraction failed: one of the source files is empty."
        ) from e

    except ValueError as e:
        raise ETLExtractionError(
            f"Extraction failed: invalid source data - {e}"
        ) from e

    except Exception as e:
        raise ETLExtractionError(
            f"Extraction failed due to an unexpected error: {e}"
        ) from e


# calling the function
if __name__ == "__main__":

    try:
        customers, orders, payments = extract_data()

        print("Extraction successful!")
        print("Customers:", customers.shape)
        print("Orders:", orders.shape)
        print("Payments:", payments.shape)

    except ETLExtractionError as e:
        print(e)