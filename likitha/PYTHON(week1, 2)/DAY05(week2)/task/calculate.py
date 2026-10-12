from statistics import mean
from employee import create_employee, display_employee
from validate import validate_age , validate_department , validate_name , validate_salary

employees=[]

def create_employee_list(count):

    for i in range(count):
        print("Enter the details of Employees:")
        employee_id = i + 101

        while True:
            name=input("Enter name of the employee:")
            if validate_name(name):
                name=name.title()
                break
            print("Invalid name.Please enter letters only")

        while True:
            try:
                age=int(input("Enter age:"))
                if validate_age(age):
                    break
                print("Age must be between 18 to 60")
            except ValueError:
                print("Age must be an integer")

        while True:
            department=input("Enter department (Data/Java/DotNet):").strip().lower()
            if validate_department(department):
                department=department.title()
                break

            print("Invalid department")

        while True:
            try:
                salary=int(input("Enter salary:"))
                if validate_salary(salary):
                    break
            except ValueError:
                print("Please enter a valid number")

        employee=create_employee(
            employee_id,
            name,
            age,
            department,
            salary
        )
        employees.append(employee)



def highest_paid_employee():
    high_paid=[employee for employee in employees if employee['gross-salary']>50000]
    for employee in high_paid:
        print(employee["name"])

salaries = [employee["gross-salary"] for employee in employees]

def display_salary_summary():
    highest_salary = max(salaries) if salaries else 0
    lowest_salary = min(salaries) if salaries else 0
    average_salary = sum(salaries) / len(salaries) if salaries else 0
    total_salary = sum(salaries)

    print("\n========== SALARY SUMMARY ==========")

    print(f"Total employees      : {len(employees)}")
    print(f"Total salary expense : ₹{total_salary:,.2f}")
    print(f"Average salary       : ₹{average_salary:,.2f}")
    print(f"Highest salary       : ₹{highest_salary:,.2f}")
    print(f"Lowest salary        : ₹{lowest_salary:,.2f}")


def display_employee_details():
    print("=============Employee details:===========\n")
    for employee in employees:
        display_employee(employee)

def bonus_increment(employee , bonus):
    return employee['gross-salary']+bonus

def tax_deduction(employee , tax):
    tax_amt=employee['gross-salary']*tax/100
    return employee['net-salary']-tax_amt

