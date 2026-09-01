# 1. ADD EXPENSE
def add_expense(expenses):
    """takes expense details from the user and adds them to the expenses list."""
    

    print("\n--- ADD EXPENSE ---")

    name = input("Enter expense name: ").strip()
    category = input("Enter category: ").strip()

    while True:
        try:
            amount = float(input("Enter amount: ₹"))

            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")

    while True:
        expense_type = input(
            "Enter type (Need/Want): "
        ).strip().title()

        if expense_type == "Need" or expense_type == "Want":
            break
        else:
            print("Please enter Need or Want.")

    expense = {
        "name": name,
        "category": category,
        "amount": amount,
        "type": expense_type
    }

    expenses.append(expense)

    print("\nExpense added successfully!")


# 2. VIEW EXPENSES
def view_expenses(expenses):
    """displays all expenses stored in the list."""
    print("\n--- ALL EXPENSES ---")

    if not expenses:
        print("No expenses added yet.")
        return

    for index, expense in enumerate(expenses, start=1):

        print(f"\nExpense {index}")
        print(f"Name     : {expense['name']}")
        print(f"Category : {expense['category']}")
        print(f"Amount   : ₹{expense['amount']:.2f}")
        print(f"Type     : {expense['type']}")


# 3. SHOW SPENDING SUMMARY
def show_summary(expenses):

    """analyzes all expenses and shows:

        Total spending
        Total Needs
        Total Wants
        Category-wise spending
        Highest spending category
    """

    print("\n--- SPENDING SUMMARY ---")

    if not expenses:
        print("No expenses available.")
        return

    total = 0
    need_total = 0
    want_total = 0
    category_totals = {}

    for expense in expenses:

        amount = expense["amount"]
        category = expense["category"]

        total += amount

        if expense["type"] == "Need":
            need_total += amount
        else:
            want_total += amount

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    highest_category = ""
    highest_amount = 0

    for category, amount in category_totals.items():

        if amount > highest_amount:
            highest_amount = amount
            highest_category = category

    print(f"\nTotal Spending: ₹{total:.2f}")
    print(f"Needs         : ₹{need_total:.2f}")
    print(f"Wants         : ₹{want_total:.2f}")

    print("\nCategory-wise Spending:")

    for category, amount in category_totals.items():
        print(f"{category}: ₹{amount:.2f}")

    print(
        f"\nHighest Spending Category: "
        f"{highest_category} (₹{highest_amount:.2f})"
    )


# 4. DETECT MONEY LEAK
def detect_money_leak(expenses, limit=200):


    """
        If you made 3 or more Want purchases in the same category, 
        the program flags it as a possible money leak.
    """
    print("\n--- MONEY LEAK DETECTOR ---")

    if not expenses:
        print("No expenses available.")
        return

    small_expense_total = 0
    small_expense_count = 0
    want_categories = {}

    for expense in expenses:

        amount = expense["amount"]
        category = expense["category"]

        if amount <= limit:
            small_expense_total += amount
            small_expense_count += 1

        if expense["type"] == "Want":

            if category not in want_categories:
                want_categories[category] = {
                    "count": 0,
                    "total": 0
                }

            want_categories[category]["count"] += 1
            want_categories[category]["total"] += amount

    print(
        f"\nSmall Expenses (≤ ₹{limit}): "
        f"{small_expense_count}"
    )

    print(
        f"Total Small Expense Spending: "
        f"₹{small_expense_total:.2f}"
    )

    print("\nPossible Money Leaks:")

    leak_found = False

    for category, data in want_categories.items():

        if data["count"] >= 3:

            leak_found = True

            print(f"\nCategory: {category}")
            print(f"Number of Purchases: {data['count']}")
            print(f"Total Spent: ₹{data['total']:.2f}")

    if not leak_found:
        print("No major repeated Want spending detected.")

    print(
        "\nNote: Small expenses can add up over time."
    )



    print("\n--- SAVINGS OPPORTUNITY ---")

    if not expenses:
        print("No expenses available.")
        return

    want_total = 0

    for expense in expenses:

        if expense["type"] == "Want":
            want_total += expense["amount"]

    monthly_savings = (
        want_total * saving_percent / 100
    )

    yearly_savings = monthly_savings * 12

    print(f"\nTotal Want Spending: ₹{want_total:.2f}")

    print(
        f"\nIf you reduce Want spending "
        f"by {saving_percent}%:"
    )

    print(
        f"Possible Savings: ₹{monthly_savings:.2f}"
    )

    print(
        f"Estimated Yearly Savings: ₹{yearly_savings:.2f}"
    )