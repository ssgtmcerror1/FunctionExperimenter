from Experiment import *
import pandas as pd
import numpy as np
from itertools import *
########################################################################################################################
# Project Name: FunctionExperimenter
# Authors: Andrew Penland and David Walsh
# Date: January 1, 2019
# Description: FunctionExperimenter is a python class that allows for the evaluation of functions on repeated orbits.
# The class accepts a function and a list of initial values. The class then evaluates it to the specified orbit and
# records the various statistics specified in the variable list and optional arguments.
########################################################################################################################

########################################################################################################################
# Class Arguments:
#   function: The function to be applied to each initial value.
#   initial_values: A list of values to be evaluated.
#   orbit_length: The orbit to evaluate each value out to.
#   var_list: A list of functions to evaluate on each initial value.
#   file_to_write: Name of csv to save results to.
#   optional_arguments: Any optional arguments to check for:
#       check_greater: Compares each previous result values and records if the value is greater than or less than
#       check_binary: Evaluates the binary value of each result value and measures the binary weight
#       check_orbit_average: Evaluates the orbit average on the initial values
########################################################################################################################


class Collatz(Experiment):

    def __init__(self, function, initial_values, orbit_length, file_to_write, optional_arguments):
        # optional arguments
        self.optional_arguments = optional_arguments
        self.check_binary = 0
        self.check_greater = 0
        self.check_orbit_average = 0
        self.check_binary_weight = 0
        super().__init__(function, initial_values, orbit_length, file_to_write)
        self.set_optional_arguments()
        self.csv_header = self.parse_headers()
        self.df = pd.DataFrame(columns=self.csv_header)

    def parse_headers(self):
        # original function
        csv_header = []
        csv_header.extend([self.function_name + "[" + str(i) + "]" for i in range(0, self.orbit_length+1)])

        # binary weight
        for i in range(0, self.orbit_length+1):
                csv_header.append("x" + str(i) + "_binary_zero_count")
                csv_header.append("x" + str(i) + "_binary_one_count")
                csv_header.append("x" + str(i) + "_binary_percent_zero")
                csv_header.append("x" + str(i) + "_binary_percent_one")

        # greater than
        # headers_chunked = list(self.chunks(csv_header, self.orbit_length+1))
        #
        # for header_list in headers_chunked:
        #     last_item = None
        #     for item in header_list:
        #         if last_item is None:
        #             item_string = str(item) + ">" + str(item)
        #         else:
        #             item_string = str(item) + ">" + str(last_item)
        #
        #         last_item = item
        #         csv_header.append(item_string)
        #
        #     csv_header.append("percent_true")
        #     csv_header.append("percent_false")

        # average
        # csv_header.append(self.function_name + "_average")

        # print(csv_header)
        return csv_header

    def run(self):

        # For each initial value, apply the function and each function.
        for value in self.init_values:
            row, result = [value], value
            for i in range(0, self.orbit_length):
                row.append(self.memoized_function(result))
                result = self.memoized_function(result)
            function_results = row

            row.extend([self.binary_weight(value) for value in function_results])
            print(row)
            # row.extend(self.is_greater(function_results))
            # row.append(self.orbit_average(function_results))

            # self.df.loc[len(self.df)] = row
            # print(self.csv_header)

        # self.df.to_csv(self.file_to_write, columns=self.csv_header, index=False, header=self.csv_header)

    def set_optional_arguments(self):
        if any("check_greater" in s for s in self.optional_arguments):
            self.check_greater = 1

        # enable binary weight
        if any("check_orbit_average" in s for s in self.optional_arguments):
            self.check_orbit_average = 1

        # enable orbit averages
        if any("check_binary" in s for s in self.optional_arguments):
            self.check_binary_weight = 1

    # Calculates the binary weight of each value in a list and measures the percentage of 1's and 0's in the value.
    def binary_weight(self, value):
        # Chunk the list in to groups of orbit length.
        # binary_list = list(self.chunks(list_of_values, self.orbit_length+1))
        # binary_weight_list = []
        #
        # for function_results in binary_list:
        #     for value in function_results:
        #         binary_value = bin(int(value))[2:]
        #         zero_count = binary_value.count("0")
        #         one_count = binary_value.count("1")
        #         zero_percent = (zero_count/(zero_count+one_count))*100
        #         one_percent = (one_count/(zero_count+one_count))*100
        #
        #         binary_weight_list.append(zero_count)
        #         binary_weight_list.append(one_count)
        #         binary_weight_list.append(round(zero_percent, 2))
        #         binary_weight_list.append(round(one_percent, 2))

        binary_weight = []
        binary_value = bin(int(value))[2:]
        zero_count = binary_value.count("0")
        one_count = binary_value.count("1")
        binary_weight.append(zero_count)
        binary_weight.append(one_count)
        binary_weight.append(zero_count/(zero_count+one_count)*100)
        binary_weight.append(one_count/(zero_count+one_count)*100)

        return binary_value.count("0"), \
               binary_value.count("1"), \
               (zero_count/(zero_count+one_count)*100), \
               (one_count/(zero_count+one_count)*100)




    # Calculates the orbit average of each initial value
    def orbit_average(self, list_of_values):
        return np.mean(list_of_values)

    def is_greater(self):
        pass

    # Helper function for chunking results.
    # l is the length of the list
    # n is the number of chunks desired
    @staticmethod
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

