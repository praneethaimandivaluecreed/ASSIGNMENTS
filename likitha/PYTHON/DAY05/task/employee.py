def create_employee(employee_id,
            name,
            age,
            department,
            salary):

    return {'employee_id':employee_id,
     'name':name,
     'age':age,
     'department':department,
     'gross-salary':salary,
     'net-salary':salary}

def display_employee(employee):
    print(
        f"ID: {employee['employee_id']} | "
        f"Name: {employee['name']} | "
        f"Age: {employee['age']} | "
        f"Department: {employee['department']} | "
        f"GrossSalary: ₹{employee['gross-salary']:.2f} |"
        f"NetSalary: ₹{employee['net-salary']:.2f}"
    )


