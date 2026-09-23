x = "GLOBAL"
 
def outer_scope():

    x = "OUTER_LOCAL"

    closures = []

    for x in ("ITER_1", "ITER_2", "ITER_3"):

        def make_closure():

            x = "CLOSURE_LOCAL"

            def inner():

                nonlocal x

                x = "MUTATED"

                return x

            return inner

        closures.append(make_closure())

    return closures, x
 
funcs, final_outer_x = outer_scope()

result_1 = funcs[0]()

result_2 = funcs[1]()
print(result_1)
print(result_2)