Employees = []
Transactions = []


def createEmployee():

    while True:
        employee_id = input("Enter employee id(EXXX): ").strip()

        if employee_id == "":
            print("Employee ID should not be empty")
            continue

        break

    while True:
        employee_name = input("Enter employee name: ").strip()

        if employee_name == "":
            print("Employee name should not be empty")
            continue

        break

    while True:
        department = input("Enter department: ").strip()

        if department == "":
            print("Department should not be empty")
            continue

        break

    while True:
        try:
            salary = float(input("Enter salary: ").strip())

            if salary <= 0:
                print("Enter valid amount")
                continue

        except ValueError:
            print("Enter valid salary")
            continue

        break

    employee = {
        'employee_id': employee_id,
        'employee_name': employee_name,
        'department': department,
        'salary': salary
    }

    Employees.append(employee)

    print("Employee created successfully")


def displayEmployees():

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


def searchEmployee(id):

    for employee in Employees:

        if employee['employee_id'] == id:
            print(
                f"ID: {employee['employee_id']} | "
                f"Name: {employee['employee_name']} | "
                f"Department: {employee['department']} | "
                f"Salary: {employee['salary']:.2f}"
            )

            return employee

    print("Employee not found")
    return None


def employeeExists(id):

    isExists = False

    for employee in Employees:

        if employee['employee_id'] == id:
            isExists = True
            break

    return isExists


def createTransaction():

    while True:

        transactionID = input("Enter transaction id(TXXX): ").strip()

        if transactionID == "":
            print("Transaction ID cannot be empty")
            continue

        break

    while True:

        employeeID = input("Enter employee id(EXXX): ").strip()

        if employeeID == "":
            print("Employee ID cannot be empty")
            continue

        if not employeeExists(employeeID):
            print("Employee does not exist")
            print("Transaction cannot be created")
            continue

        break

    while True:

        try:
            amount = float(input("Enter amount: ").strip())

            if amount <= 0:
                print("Enter valid amount")
                continue

        except ValueError:
            print("Invalid amount. Enter valid amount")
            continue

        break

    while True:

        transaction_type = input(
            "Enter transaction type(Credit/Debit): "
        ).strip().capitalize()

        if transaction_type == "":
            print("Transaction type should not be empty")
            continue

        if transaction_type != "Credit" and transaction_type != "Debit":
            print("Transaction type must be Credit or Debit")
            continue

        break

    transaction = {
        'transaction_id': transactionID,
        'employee_id': employeeID,
        'amount': amount,
        'transaction_type': transaction_type
    }

    Transactions.append(transaction)

    print("Transaction created successfully")


def displayTransactions():

    print("---------- Transaction Details ----------")

    if len(Transactions) == 0:
        print("No transactions found")
        return

    for transaction in Transactions:
        print(
            f"{transaction['transaction_id']} | "
            f"{transaction['employee_id']} | "
            f"{transaction['amount']:.2f} | "
            f"{transaction['transaction_type']}"
        )


def transactionSummary():

    while True:

        employeeID = input("Enter employee id(EXXX): ").strip()

        if employeeID == "":
            print("Employee ID cannot be empty")
            continue

        if not employeeExists(employeeID):
            print("Employee does not exist")
            continue

        break

    employeeName = ""

    for employee in Employees:

        if employee['employee_id'] == employeeID:
            employeeName = employee['employee_name']
            break

    totalCredit = 0
    totalDebit = 0

    for transaction in Transactions:

        if transaction['employee_id'] == employeeID:

            if transaction['transaction_type'] == "Credit":
                totalCredit += transaction['amount']

            elif transaction['transaction_type'] == "Debit":
                totalDebit += transaction['amount']

    netAmount = totalCredit - totalDebit

    print("---------- Transaction Summary ----------")
    print(f"Employee ID: {employeeID}")
    print(f"Employee Name: {employeeName}")
    print(f"Total Credit: {totalCredit:.2f}")
    print(f"Total Debit: {totalDebit:.2f}")
    print(f"Net Amount: {netAmount:.2f}")


while True:

    print()
    print("1. Create Employee")
    print("2. Display Employees")
    print("3. Search Employee")
    print("4. Create Transaction")
    print("5. Display Transactions")
    print("6. Transaction Summary")
    print("7. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        createEmployee()

    elif choice == "2":
        displayEmployees()

    elif choice == "3":

        employeeID = input("Enter employee id: ").strip()

        if employeeID == "":
            print("Employee ID cannot be empty")
        else:
            searchEmployee(employeeID)

    elif choice == "4":
        createTransaction()

    elif choice == "5":
        displayTransactions()

    elif choice == "6":
        transactionSummary()

    elif choice == "7":
        print("Exiting program...")
        break

    else:
        print("Invalid choice")