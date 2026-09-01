def validate_name(name):
    name = name.strip()

    if not name:
        return False
    if not name.replace(" ", "").isalpha():
        return False
    return True

def validate_age(age):
    return 18 <= age <= 60


def validate_salary(salary):
    return salary > 0


def validate_department(department):
    allowed_departments = {"data", "java", "dotnet"}

    return department.lower() in allowed_departments