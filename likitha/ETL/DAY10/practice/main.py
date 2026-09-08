from etl.extract import extract_product , extract_user
from etl.transform import transform_product , transform_user
from etl.load import load_data


def run_pipeline():

    print("Starting pipeline")
    # EXTRACT
    product_df = extract_product()
    user_df = extract_user()

    print('Staarting transformation')

    # TRANSFORM
    product_df = transform_product(product_df)
    user_df = transform_user(user_df)

    print('Loading to SQL Server')

    # LOAD
    load_data(product_df, user_df)

    print('ETL pipeline completed')

if __name__=='__main__':
    run_pipeline()
