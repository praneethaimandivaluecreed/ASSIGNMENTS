from expense_manager import (
    add_expense,
    view_expenses,
    show_summary,
    detect_money_leak,
    
)


expenses = []


def show_menu():

    print("\n" + "=" * 45)
    print("       LOST MONEY DETECTOR")
    print("=" * 45)

    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Spending Summary")
    print("4. Detect Money Leak")
    print("6. Exit")


while True:

    show_menu()

    choice = input("\nEnter your choice (1-6): ").strip()

    if choice == "1":

        add_expense(expenses)
        input("\nPress Enter to return to the menu...")

    elif choice == "2":

        view_expenses(expenses)
        input("\nPress Enter to return to the menu...")

    elif choice == "3":

        show_summary(expenses)
        input("\nPress Enter to return to the menu...")

    elif choice == "4":

        detect_money_leak(expenses)
        input("\nPress Enter to return to the menu...")


    elif choice == "5":

        print("\nThank you for using Lost Money Detector!")
        break

    else:

        print("\nInvalid choice. Please select a number from 1 to 6.")
        input("\nPress Enter to try again...")