a = 1  # Global variable

def f():
    print("f():", a)  # Uses global a

def g():
    a = 2  # Local shadows global
    print("g():", a)

def h():
    global a
    a = 3  # Modifies global a
    print("h():", a)

print("global:", a)
f()
print("global:", a)
g()
print("global:", a)
h()
print("global:", a)



# Causes error UnboundLocalError
# def fun():
#     s += ' GFG'   # Error: Python thinks s is local
#     print(s)

# s = "I love GeeksforGeeks"
# fun()


############ Local Variable Overshadowing Global Variable#########################
def fun():                                                                  
    s = "Me too."                                                                       
    print(s)
s = "I love Geeksforgeeks"
fun()   
print(s)


##############Shared Reference############################ mUTABLE OBJECTS , but for immutable no risk of data change in another variable.
L1 = [1, 2, 3, 4, 5]
L2 = L1
L1[0] = 0
print(L1)
print(L2)
