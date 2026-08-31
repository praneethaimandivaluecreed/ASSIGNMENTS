
while True:
    
    employeeID = input("Enter Employee ID: ").strip()
    if employeeID == "":
        print("Employee ID cannot be empty")
        continue
    break

while True:     
    employeeName = input("Enter Employee Name: ").strip()
    if employeeName == "":
        print("name should be entered")
        continue
    break

while True:
    try:
        age = int(input("Enter Employee age: ").strip())
        if age<18 or age > 60:
            print("Age must be between 18 and 60")
            continue
    except ValueError:
        print("Age must be valid number")
        continue
    break

while True:
    try:
        salary = float(input("Enter Employee Salary: ").strip())
        if salary < 0:
            print("Salary cannot be negative")
            continue
    except ValueError:
        print("Enter valid salary")
        continue
    break
print("Employee details created sucessfully")
print(f'Employee Details: ID: {employeeID}, Name: {employeeName}, Age: {age}, Salary: {salary:.2f}')
