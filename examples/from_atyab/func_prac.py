print("Starting the program")

# WE ARE JUST DEFINING A FUNCTION AND NOT USING/CALLING IT
# A Function uses the same formula on different data and processes it and returns an output value
# num1, num2 are function parameters (input to the function)
def calc_sum(num_1, num_2):  # Function definition
  a = num_1 + num_2  # Processing the inputs, arguments
  return a  # Returning the output value

# Substitute the return value with calc_sum(5, 10)
result = calc_sum(5, 10)

print("Result of Sum is: ", result)
print("Ending the program")