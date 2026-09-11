# here is the part of transformation in our pipeline
# here we transform the extracted data

import pandas as pd

# tranform fxn
import pandas as pd


def transform_data(customers, orders, payments):

    # -----------------------------
    # 1. Clean Customers
    # -----------------------------

    customers = customers.copy()

    # Remove duplicate customers
    customers = customers.drop_duplicates(
        subset=["CustomerID"]
    )

    # Handle missing values
    customers["Name"] = customers["Name"].fillna("Unknown")
    customers["City"] = customers["City"].fillna("Unknown")

    # Remove extra spaces
    customers["Name"] = customers["Name"].str.strip()
    customers["City"] = customers["City"].str.strip()

    # Standardize text
    customers["Name"] = customers["Name"].str.title()
    customers["City"] = customers["City"].str.title()

    # Validate/fix invalid ages
    customers.loc[
        (customers["Age"] < 18) | (customers["Age"] > 100),
        "Age"
    ] = None

    customers["Age"] = customers["Age"].fillna(
        customers["Age"].median()
    )


    # -----------------------------
    # 2. Clean Orders
    # -----------------------------

    orders = orders.copy()

    # Remove duplicate orders
    orders = orders.drop_duplicates(
        subset=["OrderID"]
    )

    # Handle missing product
    orders["Product"] = orders["Product"].fillna("Unknown")

    # Remove extra spaces
    orders["Product"] = orders["Product"].str.strip()

    # Convert OrderDate to datetime
    orders["OrderDate"] = pd.to_datetime(
        orders["OrderDate"],
        errors="coerce"
    )

    # Invalid negative amounts → missing
    orders.loc[
        orders["Amount"] < 0,
        "Amount"
    ] = None

    # Fill invalid amounts with median
    orders["Amount"] = orders["Amount"].fillna(
        orders["Amount"].median()
    )

    # Quantity must be positive
    orders.loc[
        orders["Quantity"] <= 0,
        "Quantity"
    ] = 1


    # -----------------------------
    # 3. Clean Payments
    # -----------------------------

    payments = payments.copy()

    # Remove duplicate payments
    payments = payments.drop_duplicates(
        subset=["PaymentID"]
    )

    # Handle missing payment method/status
    payments["PaymentMethod"] = payments[
        "PaymentMethod"
    ].fillna("Unknown")

    payments["PaymentStatus"] = payments[
        "PaymentStatus"
    ].fillna("Unknown")

    # Convert PaymentDate
    payments["PaymentDate"] = pd.to_datetime(
        payments["PaymentDate"],
        errors="coerce"
    )


    # -----------------------------
    # 4. Merge the datasets
    # -----------------------------

    result = orders.merge(
        customers,
        on="CustomerID",
        how="left"
    )

    result = result.merge(
        payments,
        on="OrderID",
        how="left"
    )


    # -----------------------------
    # 5. Create derived fields
    # -----------------------------

    result["OrderMonth"] = result[
        "OrderDate"
    ].dt.month

    result["OrderYear"] = result[
        "OrderDate"
    ].dt.year

    result["TotalAmount"] = (
        result["Quantity"] * result["Amount"]
    )

    return result


# calling the transform_data() function

if __name__ == "__main__":

    from extract import extract_data

    customers, orders, payments = extract_data()

    transformed_data = transform_data(
        customers,
        orders,
        payments
    )

    print("\nTransformed data:")
    print(transformed_data.head())

    print("\nShape:")
    print(transformed_data.shape)

    print("\nMissing values:")
    print(transformed_data.isnull().sum())