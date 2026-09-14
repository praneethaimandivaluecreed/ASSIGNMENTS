# here we get our transformed data and validate it
# with our business rules before loading it into the database

import pandas as pd


# custom exception for validation failures
class ETLValidationError(Exception):
    pass


def validate_data(df):

    errors = []

    # --------------------------------
    # 1. Check duplicate OrderIDs
    # --------------------------------

    if df["OrderID"].duplicated().any():
        errors.append("Duplicate OrderIDs found")

    # --------------------------------
    # 2. Check missing CustomerIDs
    # --------------------------------

    if df["CustomerID"].isnull().any():
        errors.append("Missing CustomerIDs found")

    # --------------------------------
    # 3. Check missing required fields
    # --------------------------------

    required_columns = [
        "OrderID",
        "CustomerID",
        "OrderDate",
        "Product",
        "Amount"
    ]

    for column in required_columns:

        if df[column].isnull().any():
            errors.append(
                f"Missing values found in {column}"
            )

    # --------------------------------
    # 4. Check Amount
    # --------------------------------

    if (df["Amount"] < 0).any():
        errors.append(
            "Negative order amounts found"
        )

    # --------------------------------
    # 5. Check Quantity
    # --------------------------------

    if (df["Quantity"] <= 0).any():
        errors.append(
            "Invalid quantity values found"
        )

    # --------------------------------
    # 6. Check dates
    # --------------------------------

    if df["OrderDate"].isnull().any():
        errors.append(
            "Invalid OrderDate values found"
        )

    # --------------------------------
    # Final result
    # --------------------------------

    if errors:

        print("Validation FAILED")

        for error in errors:
            print("-", error)

        # Stop the pipeline
        raise ETLValidationError(
            "Validation failed. Data will not be loaded."
        )

    else:

        print("Validation PASSED")

        return True


# Test validation

if __name__ == "__main__":

    from extract import extract_data
    from transform import transform_data

    try:

        customers, orders, payments = extract_data()

        transformed_data = transform_data(
            customers,
            orders,
            payments
        )

        is_valid = validate_data(transformed_data)

        print("\nCan data be loaded?", is_valid)

    except ETLValidationError as e:

        print("\nValidation Error:", e)

    except Exception as e:

        print("\nUnexpected Error:", e)