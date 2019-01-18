from Experiment import *


def x_plus_one(x):
    return x+1

def x_mod_four(x):
    return x % 4

# 2,3,4
# 3,4,5
# 4,5,6


new_function = Experiment(x_plus_one, ['1', '2', '3'], 4, ['a', 'b', 'c'], "somefile.csv")
y = new_function.apply_function_orbit()
print(y)

new_function_two = Experiment(x_mod_four, ['1', '2', '3'], 4, ['a', 'b', 'c'], "somefile.csv")
z = new_function_two.apply_function_orbit()
print(z)

