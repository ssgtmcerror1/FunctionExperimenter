import csv
import itertools

# FunctionExperimenter class
# Andrew Penland and David Walsh, 2019

# The objective of this class is to record data about repeated functions.


class Experiment:

    # constructor
    def __init__(self, function, initial_values, orbit_length, var_list, file_to_write, optional_arguments):
        # class variables
        self._check_greater = 0
        self._check_binary_weight = 0
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

    # this function does the main work of the class. Opens a csv, evaluates each initial value,
    # and apply var functions, then writes them to the csv file.
    def apply_function_orbit(self):
        value_results = []

        # opens the csv file passed in for writing the results
        file = open(self._file_to_write, 'w', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(self._csv_header)

            # for each initial value, apply the function and each var function
            for value in self._init_values:
                # get first value
                last_result = float(value)
                value_results.append(float(value))

                orbit_counter = 0
                # for each initial value evaluate out to the orbit length
                while orbit_counter < self._orbit_length:
                    function_result = self._evaluate_function(last_result)
                    value_results.append(float(function_result))
                    orbit_counter += 1
                    last_result = function_result

                # stores the var function results and then appends them to the results to the evaluated function
                # results for each value
                if len(self._var_list) > 0:
                    var_temp = []

                    for var_function in self._var_list:
                        for evaluated_result in value_results:
                            var_result = var_function(evaluated_result)
                            var_temp.append(var_result)
                    row = value_results + var_temp
                else:
                    row = value_results

                # check to see if each value is greater
                if self._check_greater == 1:
                    row.extend(self.is_greater(value_results + var_temp))

                # calculate binary weight
                if self._check_binary_weight == 1:
                    row.extend(self.binary_weight(value_results + var_temp))

                # writes each row of results to the csv file
                print(row)
                writer.writerow(row)

                # reset value results for next iteration
                value_results = []

        # csv is closed

        return value_results

    def orbit_headers(self):
        orbit_header_string = []

        for i in range(0, self._orbit_length+1):
            orbit_header_string.append('x' + str(i))

        return orbit_header_string

    # run function that is called from driver code
    def run(self):

        # generate orbit headers
        orbit_header = self.orbit_headers()
        var_list_header = self.parse_var_list_names()
        self._csv_header = orbit_header + var_list_header

        # check for greater then headers
        if self._check_greater == 1:
            self.parse_is_greater_headers()

        if self._check_binary_weight == 1:
            self.parse_binary_weight_headers()

        # evaluate function passed on each initial value
        self._evaluate_function_results = self.apply_function_orbit()

        # print(self._csv_header)

    # parses the var list which is later used to append to the csv headers
    def parse_var_list_names(self):
        var_list = []

        for item in self._var_list:
            for i in range(0, self._orbit_length+1):
                var_list.append(item.__name__ + "_" + str(i))

        return var_list

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

    def is_greater(self, list_of_values):
        greater_list = list(self.chunks(list_of_values, self._orbit_length+1))
        is_greater_list = []
        true_count = 0
        false_count = 0

        for function_results in greater_list:
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
                last_value = value

            percent_true = (true_count/(true_count+false_count))*100
            percent_false = (false_count/(true_count+false_count))*100
            is_greater_list.append(round(percent_true, 2))
            is_greater_list.append(round(percent_false, 2))

        return is_greater_list

    def binary_weight(self, list_of_values):
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

        return binary_weight_list

    @staticmethod
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]
