from data import Employees
from validation import get_non_empty_input, get_positive_float


def create_employee():

    employee_id = get_non_empty_input(
        "Enter employee id(EXXX): ",
        "Employee ID should not be empty"
    )

    employee_name = get_non_empty_input(
        "Enter employee name: ",
        "Employee name should not be empty"
    )

    department = get_non_empty_input(
        "Enter department: ",
        "Department should not be empty"
    )

    salary = get_positive_float("Enter salary: ")

    employee = {
        "employee_id": employee_id,
        "employee_name": employee_name,
        "department": department,
        "salary": salary
    }

    Employees.append(employee)

    print("Employee created successfully")


def display_employees():

    print("---------- Employee Details ----------")

    if len(Employees) == 0:
        print("No employees found")
        return

    for employee in Employees:
        print(
            f"ID: {employee['employee_id']} | "
            f"Name: {employee['employee_name']} | "
            f"Department: {employee['department']} | "
            f"Salary: {employee['salary']:.2f}"
        )


def search_employee(employee_id):

    for employee in Employees:

        if employee["employee_id"] == employee_id:

            print(
                f"ID: {employee['employee_id']} | "
                f"Name: {employee['employee_name']} | "
                f"Department: {employee['department']} | "
                f"Salary: {employee['salary']:.2f}"
            )

            return employee

    print("Employee not found")
    return None


def employee_exists(employee_id):

    for employee in Employees:

        if employee["employee_id"] == employee_id:
            return True

    return False