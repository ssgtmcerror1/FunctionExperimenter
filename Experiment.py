import csv

########################################################################################################################
# Project Name: FunctionExperimenter
# Authors: Andrew Penland and David Walsh
# Date: January 1, 2019
# Description: FunctionExperimenter is a python class that allows for the evaluation of function on repeated orbits.
# The class accepts a function and a list of initial values. The class then evaluates it to the specified orbit and
# records the various statistics specified in the variable list and option arguments.
########################################################################################################################

########################################################################################################################
# Class Arguments:
#   function: The function to be applied to each initial value.
#   initial_values: A list of values to be evaluated.
#   orbit_length: The orbit to evaluated each value out to.
#   var_list: A list of functions to evaluate on each initial value.
#   file_to_write: Name of csv to save results to.
#   optional_arguments: Any optional arguments to check for:
#       check_greater: Compares each previous result values and records if the value is greater than or less than
#       check_binary: Evaluates the binary value of each result value and measures the binary weight
########################################################################################################################


class Experiment:

    # Class Constructor
    def __init__(self, function, initial_values, orbit_length, var_list, file_to_write, optional_arguments):
        # option argument flags
        self._check_greater = 0
        self._check_binary_weight = 0

        # class variables
        self._csv_header = []
        self._is_greater_header = []
        self._evaluate_function = function
        self._evaluate_function_results = []
        self._function_name = function.__name__
        self._file_to_write = file_to_write
        self._init_values = initial_values.copy()
        self._orbit_length = orbit_length
        self._optional_arguments = optional_arguments.copy()
        self._var_list_results = []
        self._var_list = var_list.copy()

        # enable is greater comparison
        if any("check_greater" in s for s in optional_arguments):
            self._check_greater = 1

        # enable binary weight
        if any("check_binary" in s for s in optional_arguments):
            self._check_binary_weight = 1

    # This function does the main work of the class. Opens a csv, evaluates each initial value,
    # and applies the var functions. Finally it writes them to the csv file.
    def apply_function_orbit(self):
        # This list stores the final results and statistics for each value
        value_results = []

        # Opens the csv file passed in for writing the results
        file = open(self._file_to_write, 'w', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(self._csv_header)

            # For each initial value, apply the function and each function in the var_list.
            for value in self._init_values:
                # get first value
                last_result = float(value)
                value_results.append(float(value))

                orbit_counter = 0
                # For each initial value evaluate out to the orbit length.
                while orbit_counter < self._orbit_length:
                    function_result = self._evaluate_function(last_result)
                    value_results.append(float(function_result))
                    orbit_counter += 1
                    last_result = function_result

                # Stores the var function results and then appends them to the results to the evaluated function
                # results for each value.
                if len(self._var_list) > 0:
                    var_temp = []

                    for var_function in self._var_list:
                        for evaluated_result in value_results:
                            var_result = var_function(evaluated_result)
                            var_temp.append(var_result)
                    row = value_results + var_temp
                else:
                    row = value_results

                # Check to see if each value is greater.
                if self._check_greater == 1:
                    row.extend(self.is_greater(value_results + var_temp))

                # Calculate binary weight
                if self._check_binary_weight == 1:
                    row.extend(self.binary_weight(value_results + var_temp))

                # Writes each row of results to the csv file.
                writer.writerow(row)

                # Reset the value results for next iteration.
                value_results = []

        # csv is closed
        return value_results

    def orbit_headers(self):
        orbit_header_string = []

        for i in range(0, self._orbit_length+1):
            orbit_header_string.append('x' + str(i))

        return orbit_header_string

    # The run function that is called from driver code. This is the only function needed to be called from outside
    # the class.
    def run(self):

        # Generate the orbit headers.
        orbit_header = self.orbit_headers()
        var_list_header = self.parse_var_list_names()
        self._csv_header = orbit_header + var_list_header

        # Check to see if greater than headers need to be included.
        if self._check_greater == 1:
            self.parse_is_greater_headers()

        # Check to see if binary weight headers need to be included.
        if self._check_binary_weight == 1:
            self.parse_binary_weight_headers()

        # Evaluate the function on each initial value.
        self._evaluate_function_results = self.apply_function_orbit()

    # Parses the var list which is later used to append to the csv headers.
    def parse_var_list_names(self):
        var_list = []

        for item in self._var_list:
            for i in range(0, self._orbit_length+1):
                var_list.append(item.__name__ + "_" + str(i))

        return var_list

    # Parses the greater than headers and append them to the csv header.
    def parse_is_greater_headers(self):
        greater_header = []
        headers_chunked = list(self.chunks(self._csv_header, self._orbit_length+1))

        for header_list in headers_chunked:
            last_item = None
            for item in header_list:
                if last_item is None:
                    item_string = str(item) + ">" + str(item)
                else:
                    item_string = str(item) + ">" + str(last_item)

                last_item = item
                greater_header.append(item_string)

            greater_header.append("percent_true")
            greater_header.append("percent_false")

        self._csv_header.extend(greater_header)
        return greater_header

    # Parses the binary weight headers and then append them to the csv header.
    def parse_binary_weight_headers(self):
        binary_weight_headers = []

        for i in range(0, self._orbit_length+1):
                binary_weight_headers.append("x" + str(i) + "_binary_one_count")
                binary_weight_headers.append("x" + str(i) + "_binary_zero_count")
                binary_weight_headers.append("x" + str(i) + "_binary_percent_one")
                binary_weight_headers.append("x" + str(i) + "_binary_percent_zero")

        for item in self._var_list:
            for i in range(0, self._orbit_length+1):
                binary_weight_headers.append(item.__name__ + "_" + str(i) + "_binary_one_count")
                binary_weight_headers.append(item.__name__ + "_" + str(i) + "_binary_zero_count")
                binary_weight_headers.append(item.__name__ + "_" + str(i) + "_binary_percent_one")
                binary_weight_headers.append(item.__name__ + "_" + str(i) + "_binary_percent_zero")

        self._csv_header.extend(binary_weight_headers)
        return binary_weight_headers

    # Accepts a list and compares each current value to the previous value the list.
    # Returns a list of the results contain boolean values for each element.
    # Function also calculates the percentage of boolean values of True/False (1/0)
    def is_greater(self, list_of_values):
        greater_list = list(self.chunks(list_of_values, self._orbit_length+1))
        is_greater_list = []

        for function_results in greater_list:
            true_count = 0
            false_count = 0
            last_value = None
            for value in function_results:
                if last_value is None:
                    is_greater_list.append(0)
                    false_count += 1
                elif value < last_value:
                    is_greater_list.append(0)
                    false_count += 1
                elif value > last_value:
                    is_greater_list.append(1)
                    true_count += 1
                else:
                    is_greater_list.append(0)
                    false_count += 1
                last_value = value

                try:
                    percent_true = (true_count/(true_count+false_count))*100
                    percent_false = (false_count/(true_count+false_count))*100
                except ZeroDivisionError:
                    print("Cant Divide By Zero!")
                except Exception as e:
                    print(e)

            is_greater_list.append(round(percent_true, 2))
            is_greater_list.append(round(percent_false, 2))

        return is_greater_list

    # Calculates the binary weight of each value in a list and measures the percentage of 1's and 0's in the value.
    def binary_weight(self, list_of_values):
        # Chunk the list in to groups of orbit length.
        binary_list = list(self.chunks(list_of_values, self._orbit_length+1))
        binary_weight_list = []

        for function_results in binary_list:
            for value in function_results:
                binary_value = bin(int(value))[2:]
                zero_count = binary_value.count("0")
                one_count = binary_value.count("1")
                zero_percent = (zero_count/(zero_count+one_count))*100
                one_percent = (one_count/(zero_count+one_count))*100

                binary_weight_list.append(zero_count)
                binary_weight_list.append(one_count)
                binary_weight_list.append(round(zero_percent, 2))
                binary_weight_list.append(round(one_percent, 2))

        print(binary_weight_list)
        return binary_weight_list

    # Helper function for chunking results.
    # l is the length of the list
    # n is the number of chunks desired
    @staticmethod
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]
