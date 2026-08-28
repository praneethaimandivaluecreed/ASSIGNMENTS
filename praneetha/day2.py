#1. EMPLOYEE AGE VALIDATION
try : 
    age = int(input("Enter your age : "))

    if age >= 18 and age <= 60:
        print("You are a valid employee")
    else :
        print("You are not a valid employee")

except ValueError :
    print("Invalid input. Please enter a valid number")



#2. SALARY BONUS CALCULATOR (<30,000 - 20%    30,000 - 50,0000 - 10%    >50,000 - 5%)
try : 
    salary = float(input("Enter your salary : "))
    bonus = 0
    if salary < 30000 :
        bouns += 0.2 * salary
    elif salary >= 30000 and salary <= 50000:
        bonus += 0.1 * salary
    else :
        bonus += 0.05 * salary
    print("Your bonus is : ", bonus)

except ValueError:
    print("Enter a valid salary")




#3. EMPLOYEE LOGIN VALIDATION
user_name = input("Enter your username : ")
pass_word = input("Enter your password : ")

if user_name == "admin":
    if pass_word == "python123":
        print("Login successful")
    else :
        print("Incorrect password")
else :
    print("User not found")


#4. FINDING AN EMPLOYEE
employees = ["Rahul", "Priya", "Arun", "Sneha", "Kiran"]
emp = input("Enter an employee to search in db : ")
for i in employees:
    if i == emp :
        print("Employee found!")
        break
else :
    print("Employee not found!")



