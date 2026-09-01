from calculate import *

while True:
        try:
            count=(int(input("enter number of employees:")))
            if(count > 0):
                break
            print("enter count greater than 0")
        except ValueError:
            print("enter valid integer ")
create_employee_list(count)


while True:

    print("\nHi, Employee details entry has been completed successfully.")
    print("\n========== EMPLOYEE OPERATIONS ==========")

    print(
        "1. Display all employee details\n"
        "2. Bonus increment\n"
        "3. Tax deduction\n"
        "4. Highest paid employees\n"
        "5. Display salary summary\n"
        "6. Exit"
    )

    # Option validation
    while True:
        try:
            c = int(input("\nEnter your option: "))

            if 0 < c < 7:
                break

            print("Please enter an option between 1 and 7.")

        except ValueError:
            print("Please enter a valid integer.")

    match c:

        case 1:
            display_employee_details()

        case 2:

            name = input(
                "Enter the name of the employee: "
            ).strip().title()

            employee_found = False

            for employee in employees:

                if employee["name"] == name:

                    employee_found = True

                    while True:

                        try:
                            bonus = float(
                                input("Enter bonus amount: ")
                            )

                            if bonus <= 0:
                                print(
                                    "Bonus must be greater than 0. "
                                    "Please try again."
                                )
                                continue

                            new_salary = bonus_increment(
                                employee,
                                bonus
                            )
                            employee['gross-salary']=new_salary

                            print(
                                f"{employee['name']}'s salary after bonus: "
                                f"₹{new_salary:,.2f}"
                            )

                            break

                        except ValueError:
                            print(
                                "Please enter a valid number."
                            )

                    break

            if not employee_found:
                print(f"Employee '{name}' not found.")

        case 3:

            name = input(
                "Enter the name of the employee: "
            ).strip().title()

            employee_found = False

            # Search for employee
            for employee in employees:

                if employee["name"] == name:

                    employee_found = True

                    # Validate tax percentage
                    while True:

                        try:
                            tax = float(
                                input("Enter tax percentage: ")
                            )

                            if tax < 0 or tax > 100:

                                print(
                                    "Tax percentage must be between 0 and 100. "
                                    "Please try again."
                                )

                                continue

                            # Valid tax → calculate
                            new_salary = tax_deduction(
                                employee,
                                tax
                            )
                            employee['net-salary']=new_salary
                            print(
                                f"{employee['name']}'s salary after tax deduction: "
                                f"₹{new_salary:,.2f}"
                            )

                            break

                        except ValueError:

                            print(
                                "Please enter a valid tax percentage."
                            )

                    # Employee found, so stop searching
                    break

            # Employee was never found
            if not employee_found:

                print(
                    f"Employee '{name}' not found."
                )

        case 4:
            print("\n========== HIGHEST PAID EMPLOYEES ==========")
            highest_paid_employee()


        case 5:
            display_salary_summary()

        case 6:
            print("\nThank you! Exiting the Employee Management System.")
            break
