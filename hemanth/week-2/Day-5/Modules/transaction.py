from data import Employees, Transactions
from employee import employee_exists
from validation import (
    get_non_empty_input,
    get_positive_float,
    get_transaction_type
)


def create_transaction():

    transaction_id = get_non_empty_input(
        "Enter transaction id(TXXX): ",
        "Transaction ID cannot be empty"
    )

    while True:

        employee_id = get_non_empty_input(
            "Enter employee id(EXXX): ",
            "Employee ID cannot be empty"
        )

        if not employee_exists(employee_id):
            print("Employee does not exist")
            print("Transaction cannot be created")
            continue

        break

    amount = get_positive_float("Enter amount: ")

    transaction_type = get_transaction_type()

    transaction = {
        "transaction_id": transaction_id,
        "employee_id": employee_id,
        "amount": amount,
        "transaction_type": transaction_type
    }

    Transactions.append(transaction)

    print("Transaction created successfully")


def display_transactions():

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


def transaction_summary():

    while True:

        employee_id = get_non_empty_input(
            "Enter employee id(EXXX): ",
            "Employee ID cannot be empty"
        )

        if not employee_exists(employee_id):
            print("Employee does not exist")
            continue

        break

    employee_name = ""

    for employee in Employees:

        if employee["employee_id"] == employee_id:
            employee_name = employee["employee_name"]
            break

    total_credit = 0
    total_debit = 0

    for transaction in Transactions:

        if transaction["employee_id"] == employee_id:

            if transaction["transaction_type"] == "Credit":
                total_credit += transaction["amount"]

            elif transaction["transaction_type"] == "Debit":
                total_debit += transaction["amount"]

    net_amount = total_credit - total_debit

    print("---------- Transaction Summary ----------")
    print(f"Employee ID: {employee_id}")
    print(f"Employee Name: {employee_name}")
    print(f"Total Credit: {total_credit:.2f}")
    print(f"Total Debit: {total_debit:.2f}")
    print(f"Net Amount: {net_amount:.2f}")