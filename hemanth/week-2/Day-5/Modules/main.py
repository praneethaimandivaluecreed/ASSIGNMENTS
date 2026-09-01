from employee import (
    create_employee,
    display_employees,
    search_employee
)

from transaction import (
    create_transaction,
    display_transactions,
    transaction_summary
)


def display_menu():

    print()
    print("1. Create Employee")
    print("2. Display Employees")
    print("3. Search Employee")
    print("4. Create Transaction")
    print("5. Display Transactions")
    print("6. Transaction Summary")
    print("7. Exit")


def main():

    while True:

        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_employee()

        elif choice == "2":
            display_employees()

        elif choice == "3":

            employee_id = input(
                "Enter employee id: "
            ).strip()

            if employee_id == "":
                print("Employee ID cannot be empty")
            else:
                search_employee(employee_id)

        elif choice == "4":
            create_transaction()

        elif choice == "5":
            display_transactions()

        elif choice == "6":
            transaction_summary()

        elif choice == "7":
            print("Exiting program...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()