square = lambda x : x*2

calculate_discount = lambda x,y : x - (x * (y/100))

get_grade = lambda x: "A" if x >= 90 else "B" if  x >=75 else "C" if x >= 60 else "F"

print(square(5))
print(calculate_discount(100,5))
print(get_grade(87))