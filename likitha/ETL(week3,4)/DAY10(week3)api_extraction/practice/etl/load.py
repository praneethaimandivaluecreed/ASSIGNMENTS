from sqlalchemy import create_engine
from urllib.parse import quote_plus


def get_sql_server_engine():
    server = "tcp:NICKYSLAP,1433"
    database = "DataAnalytics"
    username = "colab_user"
    password = "123456"

    connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
    )

    connection_url = (
        "mssql+pyodbc:///?odbc_connect="
        + quote_plus(connection_string)
    )

    engine = create_engine(connection_url)

    return engine


def load_data(product_df, user_df):

    engine = get_sql_server_engine()

    product_df.to_sql(
        name="products",
        con=engine,
        if_exists="replace",
        index=False
    )

    user_df.to_sql(
        name="users",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("Data loaded successfully into SQL Server.")