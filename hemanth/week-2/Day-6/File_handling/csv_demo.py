import csv

data = [
    ["id", "name", "department", "salary"],
    [101, "Rahul", "IT", 50000],
    [102, "Priya", "HR", 45000],
    [103, "Arjun", "Finance", 60000]
]

with open("data.csv","w",newline='',encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerows(data)

with open("employees.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)

with open("data.csv",'r',encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)
