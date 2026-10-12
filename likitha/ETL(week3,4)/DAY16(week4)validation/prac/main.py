import pandas as pd


# --------------------------------------------------
# 1. Dummy Employee Data
# --------------------------------------------------

employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 104, 106],
    "name": ["Rahul", "Priya", None, "Arjun", "Arjun", "Sneha"],
    "age": [25, 30, 150, 28, 28, 17],
    "department_id": [1, 2, 3, 1, 1, 99],
    "salary": [50000, 60000, -5000, 70000, 70000, 45000]
})


# --------------------------------------------------
# 2. Department Reference Data
# --------------------------------------------------

departments = pd.DataFrame({
    "department_id": [1, 2, 3],
    "department_name": ["IT", "HR", "Finance"]
})


# --------------------------------------------------
# 3. Reusable Validation Function
# --------------------------------------------------

def validate_data(df, departments):

    data = df.copy()

    # Store validation errors for every record
    data["validation_error"] = ""

    # ----------------------------------------------
    # Schema Validation
    # ----------------------------------------------

    required_columns = [
        "employee_id",
        "name",
        "age",
        "department_id",
        "salary"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # ----------------------------------------------
    # Null Checks
    # ----------------------------------------------

    data.loc[
        data["name"].isnull(),
        "validation_error"
    ] += "Name is null; "

    data.loc[
        data["employee_id"].isnull(),
        "validation_error"
    ] += "Employee ID is null; "

    data.loc[
        data["department_id"].isnull(),
        "validation_error"
    ] += "Department ID is null; "

    # ----------------------------------------------
    # Type Checks
    # ----------------------------------------------

    data.loc[
        ~data["age"].apply(
            lambda x: isinstance(x, int)
        ),
        "validation_error"
    ] += "Invalid age type; "

    data.loc[
        ~data["salary"].apply(
            lambda x: isinstance(x, (int, float))
        ),
        "validation_error"
    ] += "Invalid salary type; "

    # ----------------------------------------------
    # Range Validation
    # ----------------------------------------------

    data.loc[
        ~data["age"].between(18, 60),
        "validation_error"
    ] += "Age must be between 18 and 60; "

    data.loc[
        data["salary"] <= 0,
        "validation_error"
    ] += "Salary must be greater than 0; "

    # ----------------------------------------------
    # Duplicate Detection
    # ----------------------------------------------

    duplicate_records = data.duplicated(
        subset=["employee_id"],
        keep=False
    )

    data.loc[
        duplicate_records,
        "validation_error"
    ] += "Duplicate employee ID; "

    # ----------------------------------------------
    # Referential Integrity Check
    # ----------------------------------------------

    valid_department_ids = set(
        departments["department_id"]
    )

    data.loc[
        ~data["department_id"].isin(valid_department_ids),
        "validation_error"
    ] += "Invalid department ID; "

    # ----------------------------------------------
    # Separate Valid and Invalid Records
    # ----------------------------------------------

    valid_df = data[
        data["validation_error"] == ""
    ].copy()

    invalid_df = data[
        data["validation_error"] != ""
    ].copy()

    return valid_df, invalid_df


# --------------------------------------------------
# 4. Run Validation
# --------------------------------------------------

valid_records, invalid_records = validate_data(
    employees,
    departments
)


# --------------------------------------------------
# 5. Display Results
# --------------------------------------------------

print("VALID RECORDS")
print(valid_records)

print("\nINVALID RECORDS")
print(invalid_records)


# --------------------------------------------------
# 6. Validation Report
# --------------------------------------------------

print("\nVALID RECORD COUNT:")
print(len(valid_records))

print("\nINVALID RECORD COUNT:")
print(len(invalid_records))