lower = int(input("enter lower range:"))
higher = int(input("enter higher range:"))
print("The prime numbers are : ",end="")
for num in range(lower,higher+1):
    for i in range(2, num):
        if num % i == 0:
            break
        else:
            print(num,end="  ")
            break