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


new_function_one = Experiment(
    x_plus_one,  # function code
    [1,2],  # do 1 to 1000
    1,  # orbit length
    [x_plus_one, x_plus_one, x_plus_one],  # var list
    # is t(n) > n?
    "somefile.csv"  # csv file to save results
    )
new_function_one.run()

