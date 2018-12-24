#for now we will just hard code the math function we want to test
def evaluate(number):
    number = int(number)
    if number % 2 == 0:
        number = (number//2)
        return number
    if number % 2 == 1:
        number = ((3*number+1))
        return number

#main function    
if __name__ == "__main__": 

    orbit = int(input("What is the length of the orbit? "))
    ensemble_list = [int(x) for x in input("Enter each value in the ensemble, sperated by a space:").split()]
    ensemble_len = len(ensemble_list)
    
    for i in range(0,ensemble_len):
        #the current integer that we are operating on
        current_value = ensemble_list[i]        
        
        #variables to test if we have reached a cycle
        current_list = []
        is_cylical = 0
        
        #evaluate the current integer up to length orbit number of times
        for j in range(0,orbit):
            print(current_value, ",", sep="", end="")
            current_value = evaluate(current_value)
                        
            #if we have reached an integer that is already in the list then we have reached a cycle
            if current_value in current_list:
                print("\nStop we have reached a cycle in",j,"iterations.")
                is_cylical = 1
                break
            elif current_value not in current_list:
                #add current value to the current_list
                current_list.append(current_value)
                            
        #if not cyclical and we have reached the end of the orbit then no cycles were detected
        if(is_cylical == 0 and j == (orbit-1)):
            print("\nNo cycle detected within",orbit,"iterations.")
        
        #delete list for next iteration
        del current_list[:]
        
        print("###")