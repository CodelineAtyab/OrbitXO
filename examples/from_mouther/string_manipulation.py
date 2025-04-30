menu = True
while menu:  
    print("Main Menu:\n1. Demonstration Mode\n2. Challenge Mode\n3. Exit")
    option = input("Choose an option: ")
    if option == "1":
        print("Demonstration Mode")
        demo_mode = input("Enter a sample string: Python is powerful and easy to learn! ")
        print("Select operation:\n" \
        "1. Basic string properties\n" \
        "2. Case manipulation\n" \
        "3. Searching operations\n" \
        "4. Slicing operations\n" \
        "5. Split and join operations\n" \
        "6. Whitespace handling\n" \
        "7. Character replacement\n" \
        "8. String alignment\n" \
        "9. String validation\n" \
        "10. Formatting techniques\n" \
        "11. Return to main menu")
        
        operation = input("Choose an operation: ")
        if operation == "1":
            print("Basic string properties")
            print(f"Length of the string: {len(demo_mode)}")
            print(f"Contactination: {demo_mode + ' is great!'}")
            print(f"Reputation: {demo_mode * 3}")
        elif operation == "2":
            print("Case manipulation")
            print(f"String in uppercase: {demo_mode.upper()}")
            print(f"String in lowercase: {demo_mode.lower()}")
            print(f"String with all words capitalized: {demo_mode.title()}")
            print(f"String with swaped case: {demo_mode.swapcase()}")
        elif operation == "3":
            print("Searching operations")
            search_string = input("Enter a substring to search: ")
            if search_string in demo_mode:
                print(f"'{search_string}' found in the string.")
                print(f"First occurrence (find): {demo_mode.find(search_string)}")
                print(f"First occurrence (index): {demo_mode.index(search_string)}")
                print(f"Count of occurrences: {demo_mode.count(search_string)}")
                print(f"Starts with '{search_string}': {demo_mode.startswith(search_string)}")
                print(f"Ends with '{search_string}': {demo_mode.endswith(search_string)}")
            else:
                print(f"'{search_string}' not found in the string.")
        elif operation == "4":
            print("Slicing operations")
            print(f"Sliced string: {demo_mode[:6]}")
        elif operation == "5":
            print("Split and join operations")
            split_string = demo_mode.split()
            print(f"Split string: {split_string}")
            join_string = " ".join(split_string)
            print(f"Joined string: {join_string}")
        elif operation == "6":
            print("Whitespace handling")
            print(f"String with leading/trailing whitespace removed: '{demo_mode.strip()}'")
            print(f"String with leading whitespace removed: '{demo_mode.lstrip()}'")
            print(f"String with trailing whitespace removed: '{demo_mode.rstrip()}'")
        elif operation == "7":
            print("Character replacement")
            old_char = input("Enter character to replace: ")
            new_char = input("Enter new character: ")
            print(f"String after replacement: {demo_mode.replace(old_char, new_char)}")
        elif operation == "8":
            print("String alignment")
            print(f"Left aligned: '{demo_mode.ljust(50)}'")
            print(f"Right aligned: '{demo_mode.rjust(50)}'")
            print(f"Center aligned: '{demo_mode.center(50)}'")
        elif operation == "9":
            print("String validation")
            print(f"Is alphanumeric: {demo_mode.isalnum()}")
            print(f"Is alphabetic: {demo_mode.isalpha()}")
            print(f"Is numeric: {demo_mode.isnumeric()}")
        elif operation == "10":
            print("Formatting techniques")
            name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            print(f"Formatted string: My name is {name} and I am {age} years old." .format(name=name, age=age))
        elif operation == "11":
            print("Returning to main menu...")
            continue
    
    elif option == "2":
        print("Challenge Mode")
        print("Challenge 1: Count how many words have more than 3 letters in a given string.")
        input_string = input("Enter a string: ")
        result = len([word for word in input_string.split() if len(word) > 3])
        print(f"Number of words with more than 3 letters: {result}")
        
        print("Challenge 2: Convert 'hello world' to 'Hello-World'.")
        input_string = input("Enter a string: ")
        converted_string = "-".join(input_string.title().split())
        print(f"Converted string: {converted_string}")
        
    elif option == "3":
        print("Exiting...")
        menu = False
    else:
        print("Invalid option. Please try again.")

