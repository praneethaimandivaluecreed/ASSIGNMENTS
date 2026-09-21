import pandas as pd

from transformations import (
    clean_names,
    clean_age,
    calculate_total_amount
)


def test_clean_names_valid_data():

    df = pd.DataFrame({
        "Name": ["john", "RAHUL", " praneetha "]
    })

    result = clean_names(df)

    assert result["Name"].tolist() == [
        "John",
        "Rahul",
        "Praneetha"
    ]


def test_clean_names_missing_value():

    df = pd.DataFrame({
        "Name": ["john", None]
    })

    result = clean_names(df)

    assert result["Name"].tolist() == [
        "John",
        "Unknown"
    ]


def test_clean_age_valid_data():

    df = pd.DataFrame({
        "Age": [25, 30, 45]
    })

    result = clean_age(df)

    assert result["Age"].tolist() == [25, 30, 45]


def test_clean_age_invalid_data():

    df = pd.DataFrame({
        "Age": [17, 25, 101]
    })

    result = clean_age(df)

    assert pd.isna(result.loc[0, "Age"])
    assert result.loc[1, "Age"] == 25
    assert pd.isna(result.loc[2, "Age"])


def test_calculate_total_amount():

    df = pd.DataFrame({
        "Quantity": [2, 5],
        "Amount": [100, 50]
    })

    result = calculate_total_amount(df)

    assert result["TotalAmount"].tolist() == [
        200,
        250
    ]