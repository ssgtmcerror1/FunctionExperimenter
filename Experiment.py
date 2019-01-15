import csv
# FunctionExperimenter class
# Andrew Penland and David Walsh, 2019

# The objective of this class is to record data about repeated functions.


class Experiment:

    # constructor
    def __init__(self, function, initial_values, orbit_length, var_list, file_to_write):
        self._function = function
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
        # record each var in var_list to file_to_write
        # write the file list
        pass

    def write_csv(self):
        #write the csv file with results
        with open(self._file_to_write, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            #write column headers
            csv_writer.writerow(['1','2','3','4'])
            #write rows
            print('Successfully saved CSV!')


new_function = Experiment("x+1", ['1', '2', '3'], 3, ['a', 'b', 'c'], "somefile.csv")
print(new_function._function)
print(new_function._init_values)
print(new_function._orbit_length)
print(new_function._var_list)
print(new_function._file_to_write)
new_function.write_csv()