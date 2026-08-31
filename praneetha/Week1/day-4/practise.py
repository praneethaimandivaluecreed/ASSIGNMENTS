#list +dictioary questions
employees = [
    {"id": 1, "name": "Pranee", "department": "HR", "salary": 30000},
    {"id": 2, "name": "Niha", "department": "IT", "salary": 45000},
    {"id": 3, "name": "Kavya", "department": "IT", "salary": 50000},
    {"id": 4, "name": "Rahul", "department": "HR", "salary": 35000}
]

#1. print name and salary of every employee
for item in employees:
    print(f'{item.get("name")} : {item.get("salary")}')


# 2. find employees from IT dep
for item in employees:
    if(item.get("department") == "IT"):
        print(f'{item.get("name")}')


# 3. Calculate total and average salary
total = 0.0
for item in employees:
    total += item.get("salary")
print(f'Total Salary : {total}\n Average : {total/len(employees)}')


#4.find the highest paid employee and print his complete details
highest = employees[0]["salary"]
idx = 0

for i in range(len(employees)):
    if(employees[i]["salary"] > highest):
        highest = employees[i]["salary"]
        idx = i
print(f'The details of the employee with highest salary is : {employees[idx]}')


# 5. count employees in each department
s = {}
# for i in range(len(employees)):
#     dep = employees[i]["department"]
#     s[dep] = s.get(dep,0)+1

for i in employees:
    dep = i["department"]
    s[dep] = s.get(dep,0)+1
    
print(s)



#6. return a list containing names of employees whose salary > 40,000
p = [x["name"] for x in employees if x["salary"] > 40000]
print(p)

#7. create a dictionary comprehension of name : salary
d = {x["name"] : x["salary"] for x in employees}
print(d)