import csv
import timeit
import string

# FunctionExperimenter class
# Andrew Penland and David Walsh, 2019

# The objective of this class is to record data about repeated functions.


class Experiment:

    # constructor
    def __init__(self, function, initial_values, orbit_length, var_list, file_to_write):
        self._csv_header = []
        self._evaluate_function = function
        self._evaluate_function_results = []
        self._function_calculation_time = 0
        self._function_name = function.__name__
        self._file_to_write = file_to_write
        self._init_values = initial_values.copy()
        self._orbit_length = orbit_length
        self._var_list_results = []
        self._var_list = var_list.copy()

    def apply_function_orbit(self):
        results = []
        value_results = []

        for value in self._init_values:
            # get first value
            last_result = float(value)
            value_results.append(float(value))

            orbit_counter = 0

            while orbit_counter < self._orbit_length:
                function_result = self._evaluate_function(last_result)
                value_results.append(float(function_result))
                orbit_counter += 1
                last_result = function_result

            results.append(value_results)
            value_results = []

        print("results=", results)
        return results

    def apply_var_functions(self):
        var_results = []
        function_results = []
        index = 0

        for var_function in self._var_list:
            for value in results_list:
                current_value = var_function(results_list[value])
                function_results.append(current_value)

            var_results.append(function_results)
            function_results = []
            index += 1

        var_results.append(function_results)

        print("var_results=", var_results)
        return var_results

    def orbit_headers(self):
        orbit_header_string = []

        for i in range(0, self._orbit_length):
            orbit_header_string.append('x' + str(i))

        return orbit_header_string

    def run(self):

        self._evaluate_function_results = self.apply_function_orbit()
        self._var_list_results = self.apply_var_functions()

        # DEBUG: print name of the function code passed in
        print("Function: " + self._function_name)
        print("=======")

        # DEBUG: print csv header
        orbit_header = self.orbit_headers()
        var_list_header = self.parse_var_list_names()
        self._csv_header = orbit_header + var_list_header

        print(self._csv_header)

        # counter = 0
        # for result in self._evaluate_function_results:
        #     print('f(' + str(result[counter][0]) + ')=', end='')
        #     print(result, self._var_list_results[counter])
        #     counter += 1

        # record each var in var_list to file_to_write
        # write the file list
        # self.write_csv()

    # parses the var list which is later used to append to the csv headers
    def parse_var_list_names(self):
        var_list = []

        for item in self._var_list:
            for i in range(0, self._orbit_length):
                var_list.append(item.__name__ + "_" + str(i))

        return var_list

    # writes the csv file with results
    def write_csv(self):

        function_results = list(self.chunk_list(self._evaluate_function_results, self._orbit_length))
        var_results = list(self.chunk_list(self._var_list_results, (self._orbit_length*len(self._var_list))))

        file = open(self._file_to_write, 'w', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(self._csv_header)

            for i in range(0, len(function_results)):
                row = function_results[i] + var_results[i]
                writer.writerow(row)
