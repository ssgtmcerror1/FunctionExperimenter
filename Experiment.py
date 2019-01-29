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
        self._orbit_length = orbit_length+1
        self._var_list_results = []
        self._var_list = var_list.copy()

    @staticmethod
    def chunk_list(result_list, chunk_size):
        for i in range(0, len(result_list), chunk_size+1):
            yield result_list[i:i + chunk_size]

    def apply_function_orbit(self):
        results = []

        for value in self._init_values:
            last_result = float(value)
            orbit_counter = 0
            results.append(float(value))

            while orbit_counter <= self._orbit_length-1:
                function_result = self._evaluate_function(last_result)
                results.append(float(function_result))
                orbit_counter += 1
                last_result = function_result
        return results

    def apply_var_functions(self, result_list):
        var_results = []

        for var_function in self._var_list:
            for value in result_list:
                var_results.append(var_function(float(value)))

        print(var_results)
        return var_results

    def orbit_headers(self):
        orbit_header_string = []

        for i in range(0, self._orbit_length):
            orbit_header_string.append('x' + str(i))

        return orbit_header_string

    def run(self):
        start_time = timeit.default_timer()

        self._evaluate_function_results = self.apply_function_orbit()
        self._var_list_results = self.apply_var_functions(self._evaluate_function_results)

        end_time = timeit.default_timer()
        self._function_calculation_time = (end_time - start_time)

        # DEBUG: print name of the function code passed in
        print("Function: " + self._function_name)
        print("=======")

        # DEBUG: print csv header
        orbit_header = self.orbit_headers()
        var_list_header = self.parse_var_list_names()
        self._csv_header = orbit_header + var_list_header

        print(self._csv_header)

        # DEBUG: print function results
        function_chunked_results = list(self.chunk_list(self._evaluate_function_results, self._orbit_length))
        var_list_chunked_results = list(self.chunk_list(self._var_list_results,
                                                        (self._orbit_length * len(self._var_list))
                                                        )

                                        )
        index = 0
        for value in self._init_values:
            print('f(' + value + ')=', end='')
            print(function_chunked_results[index], var_list_chunked_results[index])
            index += 1

        # record each var in var_list to file_to_write
        # write the file list
        # self.write_csv()

        # DEBUG: print function calculation time
        print("=======")
        print("Function evaluated in %f seconds. \n" % self._function_calculation_time)

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


