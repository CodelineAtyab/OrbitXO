
# Options
menu=[' Demonstration Mode',' Challenge Mode',' Exit']

print("Main Menu:")   
for i in range(len(menu)):
    print(f"{i+1}.{menu[i]}")

choice=int(input("\nChoose an option: ")) 
print(f"\n{menu[choice-1]}")

# Demonstration Mode
if choice == 1:
  while True:
    sample=str(input("Enter a sample string: "))

    operation=[' Basic string properties',' Case manipulation',' Searching operations',' Slicing operations',' Split and join operations',' Whitespace handling',' Character replacement',' String alignment',' String validation',' Formatting techniques',' Return to main menu']
    print("\nSelect operation: ")
    for i in range(len(operation)):
       print(f"{i+1}.{operation[i]}")
       print()   
    choice = int(input("\nChoose an operation: ")) 
    print(f"\n{operation[choice-1]}:")    

# Basic string properties
    if choice == 1:
       length = len(sample)
       print(f"Length: {length} characters\n")
       
       print("Concatenation:")
       a = ", complete the task"
       result= sample + a
       print("Result:", result)

       print("Repetition:")
       word = input("Enter the word that you want to be repeated: ")
       n = int (input("how many times you want to repeat it? "))
       repeated_word = (word+ "")* n
       print("Result: ",repeated_word)

# Case manipulation
    elif choice == 2:
        print(sample.upper())
        print(sample.lower())
        print(sample.title())
        print(sample.swapcase())


# Searching operations
    elif choice == 3:
        text= input("Enter text to search:")
        print("find:", sample.find(text))
        print("count:", sample.count(text))
        print("index:", sample.index(text))
        print("startswith:", sample.startswith(text))
        print("endswith:", sample.endswith(text))


# Slicing operations
    elif choice == 4:
        print("First 6 characters:", sample[:6])
        print("Last 6 characters:", sample[-6:])
        print("Every other character:", sample[::2])
        print("Reverse string:", sample[::-1])
        print("Extract word:", sample[10:18])
     

# Split and join operations
    elif choice == 5:
        splitting=sample.split()       
        print(splitting) 
        joining=sample.join()       
        print(joining)
        partitioning=sample.partition()       
        print(partitioning)


# Whitespace handling
    elif choice == 6:
        print(sample.strip())
        print(sample.lstrip())
        print(sample.rstrip())


# Character replacement
    elif choice == 7:
        print("replace 'a' with '*':", sample.replace("a","*"))
        translation= str.maketrans("aeiou","12345")
        print("Translat vowels:", sample.translate(translation))


# String alignment
    elif choice == 8:
        print(sample.center(8))
        print(sample.ljust(8))
        print(sample.rjust(8))
    

# String validation
    elif choice == 9:
        print("Is alpha?  ", sample.isalpha())
        print("Is digit?  ", sample.isdigit())
        print("Is alnum?  ", sample.isalnum())
        print("Is space?  ", sample.isspace())
        print("Is lower?  ", sample.islower())
        print("Is upper?  ", sample.isupper())
        print("Is title?  ", sample.istitle())
       

# Formatting techniques
    elif choice == 10:
        name= input("Enter your name: ")
        age= input("Enter your age: ")

        print("Using f-strings:")
        print(f"Hello, {name}. You are {age} years old.\n")
        print("Using .format():")
        print("Hello, {}. You are {} years old.\n".format(name,age))
        print("Using operator:")
        print("Hello, %s. You are %d years old.\n".format(name,age))


# Return to main menu
    elif choice == 11:
          break 

    else:
        print("Invalid choice. please try again.")

# Challenge Mode
elif choice == 2:
    
    # challenge 1
    print("Challenge 1:")
    print("Given the string: 'The quick brown fox jumps over the lazy dog'")
    print("write code to count how many words have more than 3 letters")
    print("Hint: len([word for word in 'The quick brown fox jumps over the lazy dog'.split() if len(word) > 3])")

    solution1= input("Your solution: ")
    try:
        result1= eval(solution1)
        correct1= len([word for word in "The quick brown fox jumps over the lazy dog".split() if len(word) > 3])
        if result1 == correct1:
            print("Correct! The answer is", correct1)
        else:
            print(" Incorrect, your answer is wrong!")
    except Exception as e:
        print("There was an error in your code:", e)

# challenge 2
    print("Challenge 2:")
    print("Write code to convert 'hello world' to 'Hello-World'")
   
    solution2= input("Your solution: ")

    try:
        result2 = eval(solution2)
        correct2 = "hello world". title().replace(" ","-")

        if result2 == correct2:
            print("Correct! The answer is", correct2)
        else:
            print(" Incorrect, your answer is wrong!")
        
    except Exception as e:
        print("There was an error in your code:", e)

# Exit 
elif choice == 3:
    print("Thank you!")


else:   
    print("Try again")  

     

