def Fibonacci(n):  
   if n <= 1:  
       return n  
   else:  
       return(Fibonacci(n-1) + Fibonacci(n-2))  
num = int(input("Enter Number of Terms: "))
if num <= 0: 
   print("Please enter a positive integer")  
else:  
   print("Fibonacci sequence:")  
   for i in range(num):  
       print(Fibonacci(i))