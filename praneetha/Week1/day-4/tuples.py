# tuples practise questions
employees = (
    ("Pranee", "HR", 30000),
    ("Niha", "IT", 45000),
    ("Kavya", "IT", 50000),
    ("Rahul", "HR", 35000)
)

# 1. Accessing Tuple Elements ⭐

# Print:

# The complete details of the first employee.
# The name of the second employee.
# The salary of the last employee.

print(employees[0])
print(employees[1][0])
print(employees[3][2])

#2. Using a loop and tuple unpacking, print:

# Pranee works in HR and earns 30000
# Niha works in IT and earns 45000

for name, dep, sal in employees:
    print(f'{name} works in {dep} for {sal}')

#3&4. print names of all employees from IT and find total and average salary
nam = []
total_sal = 0.0
for name, dep, sal in employees:
    if dep == "IT":
        nam.append(name)
    total_sal += sal
print(nam)
print(f'Total salary : {total_sal} & Average salary : {total_sal/len(employees)}')


#5. find highest paid employee
highest = employees[0]

for item in employees:
    if item[2] > highest[2]:
        highest = item
print(highest)

# slicing
numbers = (10, 20, 30, 40, 50, 60)
print(numbers[:3])
print(numbers[2:5])
print(numbers[::2])
print(numbers[::-1])