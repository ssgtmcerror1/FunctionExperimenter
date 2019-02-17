from Experiment import *

def x_plus_one(x):
    return x+1


def x_times_ten(x):
    return x * 10


def x_mod_four(x):
    return x % 4


def orb_mod_four(orbit):
    # return [x % 4 for x in orbit]
    return orbit % 4


def orb_average(orbit):
    # return mean(orbit)
    pass


def collatz(number):
    number = int(number)
    if number % 2 == 0:
        number = (number//2)
        return number
    if number % 2 == 1:
        number = (3*number+1)

    return number


values = list(range(1, 1001))

new_function_one = Experiment(
    collatz,  # function code
    values,  # initial values
    5,  # orbit length
    [x_mod_four],  # var list
    "somefile.csv",  # csv file to save results
    ["check_greater", "check_binary"]  # optional arguments
    )
new_function_one.run()
