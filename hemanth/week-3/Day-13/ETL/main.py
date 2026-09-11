from extract import extract_students
from transform import transform_products
from load import load_df


def main():

    # 1.data Extraction
    filepath = "messy_student_records.json"

    extracted_df = extract_students(filepath)

    print("Data extracted successfully")
    print(f"Records extracted: {len(extracted_df)}")


    # 2.Transformation of data
    transformed_df = transform_products(extracted_df)

    print("\nData transformed successfully")
    print(f"Records after transformation: {len(transformed_df)}")

    print("\nFinal transformed data:")
    print(transformed_df.head())

    print("\nFinal data types:")
    print(transformed_df.dtypes)

    print("\nFinal null values:")
    print(transformed_df.isna().sum())


    # 3. Load
    load_df(transformed_df)


if __name__ == "__main__":
    main()