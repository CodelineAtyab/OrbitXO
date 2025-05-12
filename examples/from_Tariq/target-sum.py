x = [int(x) for x in input("Enter the numbers: ").split()]
y = int(input("what should a number pair add up to?: "))
result = []


num = len(x)
pair = num * (num - 1) // 2

i = 0
j = 1

for z in range(pair):
    a = x[i]
    b = x[j]
    if a + b == y:
      result.append((a, b))

    j += 1
    if j == num:
      i += 1
      j = i + 1
    
if result:
   print(" , ".join([f"{a} + {b}" for a, b in result]))
else: 
    print("no pairs found")
