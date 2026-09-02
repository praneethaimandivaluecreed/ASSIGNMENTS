# method overriding fxn
def add(*args):
    if len(args) == 1:
        return args[0]
    elif len(args) == 2:
        return args[0] + args[1]
    elif len(args) == 3:
        return args[0] + args[1] + args[2]
    else:
        return sum(args)

print(add(2, 3))     
print(add(2, 3, 4))    