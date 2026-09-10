import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=.\\SQLEXPRESS;"
    "DATABASE=student1;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

try:
    connection = pyodbc.connect(connection_string)

    print("Database connected successfully")

except pyodbc.Error as e:
    print("Connection Error:", e)

cursor = connection.cursor()

rows = cursor.execute('SELECT * FROM Students')
#executes the query and return result and result is associated with cursor

print(rows)
#prints cursor object 
# because above code is  cursor.execute(...) --> rows = cursor

first_row = cursor.fetchone()
print("first_row: ",first_row) #printing first row

all_rows = cursor.fetchall() #cursor maintains pointer like file,so remaining rows are printed
print("all rows: ",all_rows)

cursor.close()

cursor = connection.cursor()# reopening cursor
rows = cursor.execute('SELECT * FROM Students') 
for row in rows: #here rows(cursor) is result-set iterator
    student_id, student_name, age, department = row

    print()
    print("Student Id:", student_id)
    print("Student Name:", student_name)
    print("Age:", age)
    print("Department:", department)

cursor.close()
connection.close()