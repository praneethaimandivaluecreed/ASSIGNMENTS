while True:     
    employeeName = input("Enter Employee Name: ").strip()
    if employeeName == "":
        print("name should be entered")
        continue
    break

while True:
    try:
        basicSalary = float(input("Enter Employee Salary: ").strip())
        if basicSalary < 0:
            print("Salary cannot be negative")
            continue
    except ValueError:
        print("Enter valid salary")
        continue
    break
while True:
    try:
        bonus = float(input("Enter bonus: ").strip())
        if bonus <0:
            print("Bonus cannot be negative")
            continue
    except ValueError:
        print("Enter valid bonus")
        continue
    break
grossSalary = basicSalary + bonus

while True:
    try:
        deduction = float(input("Enter deduction: ").strip())
        if deduction < 0:
            print("Deduction amount cannot be negative")
            continue
        elif deduction >= grossSalary:
            print("Deduction amount should be less than gross salary")
            continue
    except ValueError:
        print("Enter valid Deduction amount")
        continue
    break
netSalary = grossSalary - deduction
print('-------------Employee Details: ----------------')
print(f'Employee name: {employeeName}')
print(f'Employee Salary: {basicSalary:.2f}')
print(f'Bonus: {bonus:.2f}')
print(f'Deduction amount: {deduction:.2f}')
print(f'Gross Salary: {grossSalary:.2f}')
print(f'Net Salary: {netSalary:.2f}')