for i in range(5):
    print("*****")

#code to draw a right triangle
x = input("Enter an integer: ")
for i in range(int(x)*2):
    if i%2 == 1:
        print("*"*i)

#code to draw centered symmetric triangle
y = int(input("Enter an integer: "))
q = y
for i in range(y*2):
    if i%2 == 1:
        print((" "*q)+"*"*i)
        q-=1
