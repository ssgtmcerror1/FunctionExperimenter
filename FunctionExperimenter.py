from math import *

# list of safe methods 
# safe_list = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 
#                 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 
#                 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 
#                 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 
#                 'tan', 'tanh']
#                 
# # creating a dictionary of safe methods 
# safe_dict = dict([(k, locals().get(k,3x None)) for k in safe_list])

def collatz(number):

    if number % 2 == 0:
        print(number // 2)
        return number // 2

    elif number % 2 == 1:
        result = 3 * number + 1
        print(result)
        return result

#n = input("Give me a number: ")
#while n != 1:
#    n = collatz(int(n))
  
# def function_creator(): 
#   
#     # expression to be evaluated 
#     expr = input("Enter the function(in terms of x):") 
#   
#     # variable used in expression 
#     x = int(input("Enter the value of x:")) 
#   
#     # passing variable x in safe dictionary 
#     safe_dict['x'] = x 
#   
#     # evaluating expression 
#     y = eval(expr, {"__builtins__":None}, safe_dict) 
#   
#     # printing evaluated result 
#     print("y = {}".format(y)) 
  
if __name__ == "__main__": 
    #function_creator()
    n = input("Give me a number: ")
    while n != 1:
        n = collatz(int(n))