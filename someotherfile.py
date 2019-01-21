from Experiment import *


def x_plus_one(x):
    return x+1


def x_times_ten(x):
    return x * 10


def x_mod_four(x):
    return x % 4


def collatz(number):
    number = int(number)
    if number % 2 == 0:
        number = (number//2)
        return number
    if number % 2 == 1:
        number = (3*number+1)

    return number


# new_function = Experiment(collatz, ['1.0', '2.0', '3.0'], 5, ['a', 'b', 'c'], "somefile.csv")
# new_function.run()

new_function_two = Experiment(
    x_times_ten,  # function code
    ['30', '22', '11', '19', '16'],  # initial values
    10,  # orbit length
    ['a', 'b', 'c'],  # var list
    "somefile.csv"  # csv file to save results
    )
new_function_two.run()


# new_function_three = Experiment(x_mod_four, ['1', '2', '3'], 5, ['a', 'b', 'c'], "somefile.csv")
# new_function_three.run()

