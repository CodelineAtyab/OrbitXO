x = int(input("Enter the size of the triangle: "))

for i in range(1, x + 1):
   
    output = []
    for x in range(1, i + 1):
        output.append(str(x))
    print(''.join(output))

