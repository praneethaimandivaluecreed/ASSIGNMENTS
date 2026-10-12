print("Welcome to VC transaction system")
print("Enter employee data to modify:")
name = input("Enter employee name: ")

while name == "":
    print("Name cannot be empty.")
    name = input("Enter employee name: ")


while True:
    try:
        salary = int(input("Enter your salary: "))

        if salary <= 0:
            print("Salary must be greater than 0.")
        else:
            break

    except:
        print("You need to enter a number for salary.")
gross_salary = salary
net_salary = salary
while True:

    print("\n1. Increment")
    print("2. Deduction")
    print("3. Salary Transfer")
    print("4. Exit")

    choice = input("Enter your choice: ")

    match choice:

        case "1":
            increment = float(input("Enter increment amount: "))
            gross_salary = gross_salary + increment
            net_salary = net_salary + increment
            print("Increment successful")

        case "2":
            deduction = float(input("Enter deduction amount: "))

            if deduction <= net_salary:
                net_salary = gross_salary - deduction
                print("Deduction successful")
            else:
                print("Deduction cannot be greater than salary")

        case "3":
            transfer = float(input("Enter transfer amount: "))

            if transfer <= net_salary:
                net_salary = net_salary - transfer
                print("Transfer successful")
            else:
                print("Transfer failed")

        case "4":
            print("Thank you!")
            break

        case _:
            print("Invalid choice")

    print("\nEmployee:", name)
    print("Gross Salary:", gross_salary)
    print("Net Salary:", net_salary)