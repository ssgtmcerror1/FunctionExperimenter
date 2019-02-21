import csv
import pandas as pd
########################################################################################################################
# Project Name: FunctionExperimenter
# Authors: Andrew Penland and David Walsh
# Date: January 1, 2019
# Description: FunctionExperimenter is a python class that allows for the evaluation of functions on repeated orbits.
# The class accepts a function and a list of initial values. The class then evaluates it to the specified orbit and
# records the various statistics specified in the variable list.
########################################################################################################################

########################################################################################################################
# Class Arguments:
#   function: The function to be applied to each initial value.
#   initial_values: A list of values to be evaluated.
#   orbit_length: The orbit to evaluate each value out to.
#   var_list: A list of functions to evaluate on each initial value.
#   file_to_write: Name of csv to save results to.
########################################################################################################################


class Experiment:

    # Class Constructor
    def __init__(self, function, initial_values, orbit_length, file_to_write):
        # class variables

        self.memoized_function = self.memoize(function)
        self.function_name = function.__name__
        self.file_to_write = file_to_write
        self.init_values = initial_values
        self.orbit_length = orbit_length
        self.csv_header = self.parse_headers()
        self.df = pd.DataFrame(columns=self.csv_header)

    # This function does the main work of the class. Opens a csv, evaluates each initial value,
    # and applies the var functions. Finally it writes them to the csv file.
    def run(self):
        # For each initial value, apply the function and each function in the var_list.
        for value in self.init_values:
            row, result = [value], value
            for i in range(0, self.orbit_length):
                row.append(self.memoized_function(result))
                result = self.memoized_function(result)

            self.df.loc[len(self.df)] = row

        self.df.to_csv(self.file_to_write, columns=self.csv_header, index=False, header=self.csv_header)

    def parse_headers(self):
        return [self.function_name + "[" + str(i) + "]" for i in range(0, self.orbit_length+1)]

    def memoize(self, function):
        cache = dict()

        def memoized_func(*args):
            if args in cache:
                return cache[args]
            result = function(*args)
            cache[args] = result
            return result

        return memoized_func
