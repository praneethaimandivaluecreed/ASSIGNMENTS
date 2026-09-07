###### trying global and local scope variable ########################

gvar=11
def scope_checking():
    lvar=12
    gavr=13
    print(lvar)
    print(gvar)
print(gvar)
# print(lvar)

###############################################################################################################################
# B. Analyze the Given Program
# Study the following Python program and answer the questions:

# name = "Alice"
# age = 25
# def introduce():
#   name = "Bob"
#   city = "Mumbai"
#   print(name)
#   print(city)
#  introduce()
#  print(name)
#  print(age)

# Answer the following:
# a) What will be printed by the print(name) statement inside the introduce() function?
# b) What will be printed by the print(name) statement outside the function?
# c) Is city a global or local variable?
# d) What happens if you try to write print(city) outside the introduce() function?
# e) Explain why the name inside the function does not change the global name.


###solutions################

# a) Bob
# b)Alice
# c)local variable
# d)we will get an error that city variable didnt exist
# e) because the scope of the name variable inside the function is within the function .

