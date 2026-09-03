# code demonstrating global and local varibales scope


# tomato ketchup is a global varible
global_food = "Tomato kechup"

def pizza_hut() :

    #pizza is a local variable here
    local_food = "pizza"

    # here I can access local variable inside the local scope
    print(f'I can eat {local_food} inside pizza hut')

    # I can also access global variable inside the local scope
    print(f'Hurray! I can also eat my {local_food} with my {global_food} inside pizza_hut')



#calling the fxn
pizza_hut()


#here outside the local_scope(i.e inside the global scope)

# I can access my global variable
print(f'I can have my {global_food} outside pizza hut')

# But I cannot access my local_variable outside the local scope
#print(f'Shit ! I cannot have {local_food} outside pizza hut')  # will raise an error

