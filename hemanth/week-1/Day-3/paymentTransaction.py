employee_salary = 50000
print(f"Current Salary: {employee_salary:.2f}")

while True:
    try:
        paymentAmount = float(input("Enter payment amount: ").strip())

        if paymentAmount <= 0:
            print("Payment amount must be greater than 0")
            continue

        if paymentAmount > employee_salary:
            print("Transaction failed.")
            print("Insufficient salary balance.")
            continue

    except ValueError:
        print("Payment amount must be numeric")
        continue

    break

employee_salary = employee_salary - paymentAmount

print("Payment successful.")
print(f"Remaining salary: {employee_salary:.2f}")