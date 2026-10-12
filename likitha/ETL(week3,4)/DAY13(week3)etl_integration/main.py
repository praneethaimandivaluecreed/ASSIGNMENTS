from extract import extract
from transfer import transform
from load import load


def main():

    print("ETL pipeline started.")

    data = extract()

    data = transform(data)

    load(data)

    print("ETL pipeline completed successfully.")


if __name__ == "__main__":
    main()