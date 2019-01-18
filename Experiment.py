import csv

# FunctionExperimenter class
# Andrew Penland and David Walsh, 2019

# The objective of this class is to record data about repeated functions.


class Experiment:

    # constructor
    def __init__(self, function, initial_values, orbit_length, var_list, file_to_write):
        self._evaluate_function = function
        self._init_values = initial_values.copy()
        self._orbit_length = orbit_length
        self._var_list = var_list.copy()
        self._file_to_write = file_to_write

    def orbit(self, n):
        # should return x0, x1, x2, ..., xn
        # x_{i+1} = f(x_i)
        pass

    # one major method: run the experiment
    def run(self):
        # make the function repeat function on each initial value
        # self.apply_function_orbit()
        # record each var in var_list to file_to_write
        # write the file list
        self.write_csv()
        pass

    # writes the csv file with results
    def write_csv(self):
        # open the file
        file = open(self._file_to_write, 'w')
        with file:
            writer = csv.writer(file)
            # generate the headers
            header = self.generate_csv_headers()
            writer.writerow(header)

    # generate a list of column headers with function and var list
    def generate_csv_headers(self, name):
        # empty list to store column header names
        column_headers = []

        # iterate through orbit length and append function_name + current orbit value as a string
        for i in range(0, self._orbit_length):
            column_headers.append(name + '[' + str(i) + ']')

        # get length of var_list
        length_of_var_list = len(self._var_list)
        for j in range(0, length_of_var_list):
            column_headers.append(self._var_list[j])

        return column_headers

    def apply_function_orbit(self):

        results = []
        current_result_values = []
        for i in range(0, len(self._init_values)):
            for j in range(0, self._orbit_length-1):
                # get the result of the current value applied to the function
                result = self._evaluate_function(int(self._init_values[i]) + j)
                # append result to the results_values list
                current_result_values.append(result)
                # append complete list of results to the list of results
        results.append(current_result_values)

        print(results)

