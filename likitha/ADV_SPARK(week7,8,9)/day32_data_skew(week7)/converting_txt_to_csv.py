import csv

with open("employee_records.txt" , "r", encoding="utf-8") as file:
    reader=csv.reader(file)
    with open("employee_records.csv" , "w" , newline="" , encoding="utf-8") as ofile:
        writer=csv.writer(ofile)
        writer.writerows(reader)