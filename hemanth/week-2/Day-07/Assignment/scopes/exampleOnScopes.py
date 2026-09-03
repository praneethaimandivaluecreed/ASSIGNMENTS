x = 2
y = 3
#above variables has global scope
def numbers():
    x = 20
    y = 30
    #assigned new values to x and y,but here they have local scope,so they are declared first time
    print(x +y)
    #print sum of values gives  sum of values in this function

print(x+y)
#print the sum of x and y gives sum of 2 and 3 not 20 and 30,as x,y refers to 2 and 3 which has global scope

numbers()


def global_scope():
    global x
    global y
    x = 100
    y = 200

global_scope()
#after executing above function,the variables will be reassigned at global level,so changes made in 
#func will be reflected in global level
print(x+y)

