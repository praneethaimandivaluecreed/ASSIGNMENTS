#docstring is used to document the code in function and various object entities
def sum_of_numbers(a,b):
    """This function takes two numbers and returns their sum."""
    return a + b

a = int(input("Enter a: "))
b = int(input("Enter b: "))
print(sum_of_numbers(a,b))
print("Docstring of above function: ",end=" ")
print(sum_of_numbers.__doc__)