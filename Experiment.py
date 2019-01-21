import csv
import timeit
import string

# FunctionExperimenter class
# Andrew Penland and David Walsh, 2019

# The objective of this class is to record data about repeated functions.


class Experiment:

    # constructor
    def __init__(self, function, initial_values, orbit_length, var_list, file_to_write):
        self._evaluate_function = function
        self._function_name = function.__name__
        self._file_to_write = file_to_write
        self._init_values = initial_values.copy()
        self._orbit_length = orbit_length+1
        self._var_list = var_list.copy()
        self._results = []
        self._function_calculation_time = 0

    @staticmethod
    def chunk_list(result_list, chunk_size):
        for i in range(0, len(result_list), chunk_size):
            yield result_list[i:i + chunk_size]

    def apply_function_orbit(self):
        results = []

        for value in self._init_values:
            orbit = 0
            current_value = float(value)
            while orbit <= self._orbit_length-1:
                result = self._evaluate_function(current_value+orbit)
                results.append(result)
                orbit += 1

        return results

    # generate a list of column headers with function and var list
    def generate_csv_headers(self, name):
        column_headers = []
        length_of_var_list = len(self._var_list)

        for i in range(0, self._orbit_length):
            column_headers.append(name + '[' + str(i) + ']')

        for j in range(0, length_of_var_list):
            column_headers.append(self._var_list[j])

        return column_headers

    def orbit_headers(self):
        # should return x0, x1, x2, ..., xn
        # x_{i+1} = f(x_i)

        orbit_header_string = []
        for i in range(0, self._orbit_length):
            orbit_header_string.append('x_{i+' + str(i) + '}')

        return orbit_header_string

    # one major method: run the experiment
    def run(self):
        # record start time
        start_time = timeit.default_timer()

        # make the function repeat function on each initial value
        self._results = self.apply_function_orbit()

        # calculate execution time
        end_time = timeit.default_timer()
        self._function_calculation_time = (end_time - start_time)

        # DEBUG: print name of the function code passed in
        print("Function: " + self._function_name)
        print("=======")

        # DEBUG: print orbit headers
        orbit_header = self.orbit_headers()
        print(orbit_header)

        # DEBUG: print function results
        chunked_results = list(self.chunk_list(self._results, self._orbit_length))
        index = 0

        for value in self._init_values:
            print('f(' + value + ')=', end='')
            print(chunked_results[index])
            index += 1

        # record each var in var_list to file_to_write
        # TODO: implement this

        # write the file list
        self.write_csv()

        # DEBUG: print function calculation time
        print("=======")
        print("Function evaluated in %f seconds. \n" % self._function_calculation_time)

    # writes the csv file with results
    def write_csv(self):
        file = open(self._file_to_write, 'w', newline='')
        with file:
            writer = csv.writer(file)

            # write function name
            writer.writerow(['Function: ' + self._function_name])

            # orbit headers
            field_names = self.orbit_headers()
            writer.writerow([''] + field_names)

            # write results
            results = list(self.chunk_list(self._results, self._orbit_length))
            for i in range(0, len(results)):
                writer.writerow(['f(' + str(self._init_values[i]) + ')'] + results[i])

            # header = self.generate_csv_headers()
            # writer.writerow(header)

            # function calculation time
            writer.writerow(['Function evaluated in %f seconds.' % self._function_calculation_time])

