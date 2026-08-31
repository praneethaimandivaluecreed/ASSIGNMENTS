name = input("Enter name: ")
salary = float(input("Enter salary: "))
experience = int(input("Enter years of experience: "))

bonus = 0.0

if experience <3:
    bonus = 1.15
elif experience <= 5:
    bonus = 1.3
else:
    bonus = 1.5
print("The net  salay of {0} who has {1} years of experience is {2:.2f}".format(name,experience,bonus*salary))