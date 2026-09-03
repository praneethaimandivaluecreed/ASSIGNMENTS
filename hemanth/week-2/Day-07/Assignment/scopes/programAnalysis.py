name = "Alice"
age = 25

def introduce():
 name = "Bob"
 city = "Mumbai"
 print(name)
 print(city) 

 
introduce()
print(name)
print(age)

""" What will be printed by the print(name) statement inside the introduce() function?
ANS: 
BOB
Mumbai
"""

"""
 What will be printed by the print(name) statement outside the function?
 ANS:
 Alice
25
"""

"""
Is city a global or local variable?
ANS:
local variable
"""

"""
What happens if you try to write print(city) outside the introduce() function?
ANS: 
NameError: name 'city' is not defined
"""

"""
Explain why the name inside the function does not change the global name.
ANS:

Because Name inside the function has local scope any changes made in function lies in the function,it does not 
effect globally.
"""