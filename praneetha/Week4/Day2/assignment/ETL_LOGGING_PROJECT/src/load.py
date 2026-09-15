import logging


logger = logging.getLogger(__name__)


# fxn to load data into the db
def load_data(df, connection, batch_size=40):

    logger.info(
        f"loading_start | Records: {len(df)}"
    )

    cursor = connection.cursor()

    columns = [
        "OrderID",
        "CustomerID",
        "CustomerName",
        "Age",
        "City",
        "Product",
        "Category",
        "Quantity",
        "Amount",
        "OrderDate",
        "PaymentMethod",
        "OrderMonth",
        "OrderYear",
        "TotalAmount"
    ]

    insert_query = """
        INSERT INTO ETL_Sale (
            OrderID,
            CustomerID,
            CustomerName,
            Age,
            City,
            Product,
            Category,
            Quantity,
            Amount,
            OrderDate,
            PaymentMethod,
            OrderMonth,
            OrderYear,
            TotalAmount
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    try:

        total_records = len(df)

        for start in range(0, total_records, batch_size):

            end = min(
                start + batch_size,
                total_records
            )

            batch = df.iloc[start:end]

            values = [
                tuple(row[column] for column in columns)
                for _, row in batch.iterrows()
            ]

            cursor.executemany(
                insert_query,
                values
            )

            logger.info(
                f"batch_loaded | "
                f"Records: {start + 1}-{end}"
            )

        connection.commit()

        logger.info(
            f"loading_complete | "
            f"Records loaded: {total_records}"
        )

    except Exception:

        connection.rollback()

        logger.exception(
            "loading_failed | Transaction rolled back"
        )

        raise