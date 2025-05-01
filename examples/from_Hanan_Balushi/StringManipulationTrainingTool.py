def demonestrationModeOps(selection,string):
    if selection == "1":
        print("Basic string properties: ")
        print("Length: ", len(string),"characters\n")
        print("Concatenation: ")
        next_string = input("Add a string: ")
        print("Result: "+string+" "+next_string)
        print("\nRepetition: ")
        print("Result: ",string*3)
    elif selection == "4":
        print("\nSlicing Operations:")
        print("First 6 characters: ", string[:6])
        print("\nLast 6 characters: ",string[-6:])
        print("\nEvery other character: ",string[::2])
        print("Reverse string: ",string[::-1])
    elif selection == "10":
        print("\nFormatting Techniques: ")
        print("Using f-strings: ")
        print(f"Result: the string has {len(string)} charecters")
        print("\nUsing .format(): ")
        print("Hello {name}, today is {date}".format(name="Team Code Orbit", date="01-05-2025"))
        print("\nUsing % Operator:")
        print("Result: %d%% is my grade" %90)




#starts here
print("Main Menu:\n1. Demonstration Mode\n2. Challenge Mode\n3. Exit\n\n")
main_selection = input("Choose an option: ")

while main_selection != "3":
    if main_selection == "1":
        print("DEMONSTRATION MODE")
        sample_string =  input("Enter a sample string: ")
        print("\nSelect operation:\n1. Basic string properties\n2. Case manipulation\n3. Searching operations\n4. Slicing operations\n5. Split and join operations\n6. Whitespace handling\n7. Character replacement\n8. String alignment\n9. String validation\n10. Formatting techniques\n11. Return to main menu")
        selected_operation = input("\nChoose an operation: ")
        while selected_operation != "11":
            demonestrationModeOps(selected_operation,sample_string)
            print("\nSelect operation:\n1. Basic string properties\n2. Case manipulation\n3. Searching operations\n4. Slicing operations\n5. Split and join operations\n6. Whitespace handling\n7. Character replacement\n8. String alignment\n9. String validation\n10. Formatting techniques\n11. Return to main menu")
            selected_operation = input("\nChoose an operation: ")
        print("Main Menu:\n1. Demonstration Mode\n2. Challenge Mode\n3. Exit\n\n")
        main_selection = input("\nChoose an option: ")
    else:
        print("\nCHALLENGE MODE")
        print("Challenge 1: Given the string 'The quick brown fox jumps over the lazy dog',\n\
            write code to count how many words have more than 3 letters.")
        solution = input("Your Solution (type 'hint' for a hint): ")
        if solution.lower() == "hint":
            solution = input("Use the split() method to break the sentence into words, then use a loop or list comprehension to count how many of those words have a length greater than 3. : ")
            print("Main Menu:\n1. Demonstration Mode\n2. Challenge Mode\n3. Exit\n\n")
            main_selection = input("\nChoose an option: ")
        else:
            words = [word for word in "The quick brown fox jumps over the lazy dog".split() if len(word) > 3]
            if eval(solution) == len(words):
                print(f"Correct! The answer is {len(words)} words.")
                print(f"Explanation: {words} all have more than 3 letters.")
                solution2 = input("Challenge 2: Write code to convert 'hello world' to 'Hello-World': ")
                if eval(solution2) == "Hello-World".lower():
                    print("\nWell Done!")
                    break

        