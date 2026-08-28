# printing data types of diffrent variables
age = 21
salary = 567.8
is_logged_in = True
name = 'pranee'
result = None

'''
print(type(age))
print(type(salary))
print(type(is_logged_in))
print(type(name))
print(type(result))
'''

# arithmetic operators
add = 3+4
sub = 4-3
mul = 5*6
div = 34/4
flor_div = 34//4
neg_floor = -34//4 # rounds towards -ve infinity
mod = 34 % 2
exp = 2**3

'''
print(add)
print(sub)
print(mul)
print(div)
print(flor_div)
print(neg_floor)
print(mod)
print(exp)
'''

#comparision operatorsr
a = 10
b = 20
c = "pranee"
d = 10

if(a != d): 
    print("both of them are not equal")
else : 
    print("both of them are  equal")


#logical operators (and,or,not)

age = int(input("Enter your age : "))
has_liscence =  input("Enter whether you have liscence (y/n) : ")
if age > 18 or has_liscence == 'y':
    print(f"Your age is {age} and your liscence status is {has_liscence}")
else :
    print("You are not allowed to drive!")


#string operationsss
# s = '''
# I am praneeeeetha
# currently in my btech 4th year
#     first semester
# '''
# print(s)

#indexing
# str = "praneetha Imandi"
# str2 = "Venkat"
# print(str[-2])
# print(str[2])
# print(str[3:8])
# print(str[:-5])
# #length of string
# print(len(str))
# print(str.lower()) #lower
# print(str.upper()) #upper
# print(str+" "+str2) #concat
# p = "  I am pranee "
# print(p.strip()) # strip
# print(str.replace("Imandi","Venkat")) #replace
# print("pranee" * 3)  #repetetion















# assignment prblm
try:
    name = input("Enter employee name: ")
    salary = float(input("Enter salary: "))

except ValueError:
    print("Salary must be a valid number.")

else:
    print("\nEmployee Details")
    print("-" * 25)
    print(f"Name: {name}")
    print(f"Salary: ₹{salary:,.2f}")

finally:
    print("\nThank you for using the Employee Calculator.")