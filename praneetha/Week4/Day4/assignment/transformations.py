import pandas as pd


def clean_names(df):
    df = df.copy()

    df["Name"] = df["Name"].fillna("Unknown")
    df["Name"] = df["Name"].str.strip().str.title()

    return df


def clean_age(df):
    df = df.copy()

    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

    df.loc[(df["Age"] < 18) | (df["Age"] > 100), "Age"] = None

    return df


def calculate_total_amount(df):
    df = df.copy()

    df["TotalAmount"] = df["Quantity"] * df["Amount"]

    return df