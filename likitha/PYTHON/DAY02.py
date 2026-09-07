name = input("Enter employee name: ") 
salary = float(input("Enter basic salary: ")) 
bonus = float(input("Enter bonus: ")) 
tax = float(input("Enter tax percentage: "))

gross_salary = salary + bonus 
tax_amount = gross_salary * tax / 100 
net_salary = gross_salary - tax_amount 

print("\n----- Employee Salary Report -----") 
print(f"Employee Name : {name}") 
print(f"Basic Salary  : ₹{salary:.2f}") 
print(f"Bonus         : ₹{bonus:.2f}") 
print(f"Gross Salary  : ₹{gross_salary:.2f}") 
print(f"Tax Amount    : ₹{tax_amount:.2f}") 
print(f"Net Salary    : ₹{net_salary:.2f}") 