while True:
    
    employeeID = input("Enter Employee ID: ").strip()
    if employeeID == "":
        print("Employee ID cannot be empty")
        continue
    break
while True:

    try:
        currentSalary = float(input("Enter current Salary: ").strip())
        if currentSalary < 0:
            print("Salary cannot be negative")
            continue
    except ValueError:
        print("Enter valid salary")
        continue
    break

while True:
    try:
        incrementPercent = float(input("Enter increment percent: ").strip())
        if incrementPercent < 0 or incrementPercent >100.0:
            print("Enter valid percent")
            continue
    except ValueError:
        print("Enter valid percent")
        continue
    break
incrementAmount = currentSalary * (incrementPercent/100)
newSalary = currentSalary + incrementAmount

print('-------------Employee Details: ----------------')
print(f'Employee current salary: {currentSalary:.2f}')
print(f'Employee new salary: {newSalary:.2f}')