import csv


#creating a csv file with the data
# with open("employee.csv","w", newline = "", encoding = "utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(["id", "name", "department", "salary"])
#     writer.writerow([101, "Anu", "IT", 50000])
#     writer.writerow([102, "Ravi", "HR", 45000])
#     writer.writerow([103, "Priya", "Finance", 60000])


#reading the existing csv file
with open("employee.csv", "r", newline = "",encoding = "utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        print(f"Name : {row["name"]} | Marks : {row["salary"]}")



# import csv

# with open("employee.csv", "r", newline="", encoding="utf-8") as file:
#     reader = csv.reader(file)

#     print(reader)