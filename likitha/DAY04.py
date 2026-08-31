count=int(input("Enter number of employees:"))
employees=[]
for i in range(count):
    employee={
        "name":input("Enter name of the employee:"),
        "age":int(input("Enter age fo the employee:")),
        "grosssalary":int(input("Enter grosssalary of the employee:")),
        "bonus":int(input("Enter bonus of the employee:")),
        "tax":int(input("Enter tax of the employee:"))
    }
    tax_amount = employee["grosssalary"] * employee["tax"] / 100
    employee["netsalary"] = employee["grosssalary"] - tax_amount
    employees.append(employee)


while(True):
    name=input("Enter the name of the employee to do operation with :")
    n=int(input("Select option :\n 1.bonus\n 2.deduction(tax)\n 3.View Details \n 4.exit \n"))
    s={}
    for emp in employees:
        if emp['name']==name:
            s=emp
    match n:
        case 1:
            s['grosssalary']+=s['bonus']
            s['netsalary']+=s['bonus']
        case 2:
            taxamt=s['grosssalary']* s[tax] /100
            s['netsalary']=s['grosssalary']-taxamt
        case 3:
            print(s)
        case 4:
            break
