a = 10
b = 15

print(f"Before a={a} b={b}")

# Making use of BitWise XOR to digest and undigest
a = a ^ b
b = a ^ b
a = a ^ b

print(f"After a={a} b={b}")