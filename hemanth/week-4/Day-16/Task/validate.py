import pandas as pd
from logger import logger

class ValidationError(Exception):
    pass


def validate_students(df):

    logger.info(f"Validation started: {len(df)} records")

    valid_mask = pd.Series(True, index=df.index)
    validation_reason = pd.Series("", index=df.index)

    # Validate student_id
    invalid_student_id = df["student_id"].isna()

    valid_mask &= ~invalid_student_id
    validation_reason.loc[invalid_student_id] += "Missing student_id; "

    # Validate student_name
    invalid_name = df["student_name"].isna() | (
        df["student_name"].astype(str).str.strip() == ""
    )

    valid_mask &= ~invalid_name
    validation_reason.loc[invalid_name] += "Invalid student_name; "

    # Validate age
    invalid_age = (df["age"] < 18) | (df["age"] > 60)

    valid_mask &= ~invalid_age
    validation_reason.loc[invalid_age] += "Age must be between 18 and 60; "

    # Validate gender
    valid_genders = ["Male", "Female", "Unknown"]

    invalid_gender = ~df["gender"].isin(valid_genders)

    valid_mask &= ~invalid_gender
    validation_reason.loc[invalid_gender] += "Invalid gender; "

    # Validate course
    valid_courses = [
        "Python",
        "SQL",
        "Data Science",
        "Computer Science"
    ]

    invalid_course = ~df["course"].isin(valid_courses)

    valid_mask &= ~invalid_course
    validation_reason.loc[invalid_course] += "Invalid course; "

    # Validate marks
    invalid_marks = (df["marks"] < 0) | (df["marks"] > 100)

    valid_mask &= ~invalid_marks
    validation_reason.loc[invalid_marks] += "Marks must be between 0 and 100; "

    # Validate attendance
    invalid_attendance = (
        (df["attendance"] < 0) |
        (df["attendance"] > 100)
    )

    valid_mask &= ~invalid_attendance
    validation_reason.loc[invalid_attendance] += (
        "Attendance must be between 0 and 100; "
    )

    # Validate city
    invalid_city = df["city"].isna() | (
        df["city"].astype(str).str.strip() == ""
    )

    valid_mask &= ~invalid_city
    validation_reason.loc[invalid_city] += "Invalid city; "

    # Separate valid and invalid records
    valid_df = df[valid_mask].copy()
    invalid_df = df[~valid_mask].copy()

    invalid_df["validation_reason"] = validation_reason[~valid_mask]

    logger.info(f"Valid records: {len(valid_df)}")
    logger.info(f"Invalid records: {len(invalid_df)}")

    return valid_df, invalid_df