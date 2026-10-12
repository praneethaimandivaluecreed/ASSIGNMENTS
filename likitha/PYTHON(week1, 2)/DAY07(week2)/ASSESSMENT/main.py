################## LAMBDA #####################
# 1. Convert an existing function into a lambda function.
# i) def cube(num):
# return num ** 3

# ii) def calculate_total(price, quantity):
# return price * quantity

# iii) def check_number(num):
# if num > 0:
# return "Positive"
# elif num < 0:
# return "Negative"
# else:
# return "Zero”

#######solutions

cube=lambda x: x*x
print(cube(3))

calculate_total= lambda price , quantity :price*quantity
print(calculate_total(2 , 5))

check_number=lambda num: "Positive" if num>0 else "Negative" if num<0 else "Zero"

############################################