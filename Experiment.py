import csv
import itertools

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

    @staticmethod
    def chunk_list(result_list, chunk_size):
        for i in range(0, len(result_list), chunk_size):
            yield result_list[i:i + chunk_size]

    @staticmethod
    def slice_per(source, step):
        return [source[i::step] for i in range(step)]

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

        return results

    def apply_var_functions(self):
        var_results = []
        function_results = []

        for var_function in self._var_list:
            for result_list in self._evaluate_function_results:
                for value in result_list:
                    current_value = var_function(value)
                    function_results.append(current_value)

                var_results.append(function_results)
                function_results = []

        return var_results

    def orbit_headers(self):
        orbit_header_string = []

        for i in range(0, self._orbit_length+1):
            orbit_header_string.append('x' + str(i))

        return orbit_header_string

    def run(self):

        self._evaluate_function_results = self.apply_function_orbit()
        self._var_list_results = self.apply_var_functions()

        # DEBUG: print csv header
        orbit_header = self.orbit_headers()
        var_list_header = self.parse_var_list_names()
        self._csv_header = orbit_header + var_list_header

        # print(self._csv_header)

        # record each var in var_list to file_to_write

        # write the file list
        print(self._evaluate_function_results)
        print(self._var_list_results)

        #self.write_csv()

    # parses the var list which is later used to append to the csv headers
    def parse_var_list_names(self):
        var_list = []

        for item in self._var_list:
            for i in range(0, self._orbit_length+1):
                var_list.append(item.__name__ + "_" + str(i))

        return var_list

    # writes the csv file with results
    def write_csv(self):

        l = self.slice_per(self._var_list_results, self._orbit_length)
        print(l)

        file = open(self._file_to_write, 'w', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(self._csv_header)

            for item in self._evaluate_function_results:
                # merged_vars = list(itertools.chain(*l[i]))
                row = item
                print(row)
                writer.writerow(row)
