def get_non_empty_input(prompt, error_message):
    while True:
        value = input(prompt).strip()

        if value == "":
            print(error_message)
            continue

        return value


def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt).strip())

            if value <= 0:
                print("Enter valid amount")
                continue

            return value

        except ValueError:
            print("Enter valid amount")


def get_transaction_type():
    while True:
        transaction_type = input(
            "Enter transaction type(Credit/Debit): "
        ).strip().capitalize()

        if transaction_type == "":
            print("Transaction type should not be empty")
            continue

        if transaction_type not in ("Credit", "Debit"):
            print("Transaction type must be Credit or Debit")
            continue

        return transaction_type