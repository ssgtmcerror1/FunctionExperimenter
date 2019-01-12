#decimal to binary
def DecToBin(n):
    if(n > 1):  
        DecToBin(n//2)  
    print(n % 2, end='')     

#binary to decimal
def BinToDec(n):
    d = 0
    i = 0
    while(n != 0): 
        decimal = n % 10
        d = d + decimal * pow(2,i) 
        n = n//10
        i += 1
    print(d)