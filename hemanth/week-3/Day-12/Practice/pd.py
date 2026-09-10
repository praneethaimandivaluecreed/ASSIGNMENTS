import pyodbc
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

connection_string = (
    f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_DATABASE')};"
    f"Trusted_Connection={os.getenv('DB_TRUSTED_CONNECTION')};"
    f"TrustServerCertificate={os.getenv('DB_TRUST_SERVER_CERTIFICATE')};"
)

try:
    connection = pyodbc.connect(connection_string)

    print("Database connected successfully")

except pyodbc.Error as e:
    print("Connection Error:", e)

cursor = connection.cursor()
cursor.execute("SELECT * FROM Students")
rows = cursor.fetchall()



print(cursor.description) #gives you metadata about each column.
#(column_name,type_code,display_size,internal_size,precision,scale,null_ok)

for row in rows:
    print(row)

columns = [column[0] for column in cursor.description]
print(columns)

df = pd.DataFrame.from_records(rows,columns=columns)
print(df)

df = pd.read_sql(
    "SELECT * FROM Students",
    connection
)

print(df)