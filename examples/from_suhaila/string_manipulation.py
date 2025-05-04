menu = True
while menu:
    print("Main Menu:\n1. Demonstration Mode\n2. Challenge Mode\n3. Exit")
    option = input("Choose an option: ")
    if option == "1":
        print("Demonstration Mode")
        demo_string = input("Enter a sample string: Python is powerful and easy to learn! ")
        print("Select operation:")
        print("1. Basic string properties")
        print("2. Case manipulation")
        print("3. Searching operations")
        print("4. Slicing operations")
        print("5. Split and join operations")
        print("6. Whitespace handling")
        print("7. Character replacement")
        print("8. String alignment")
        print("9. String validation")
        print("10. Formatting techniques")
        print("11. Return to main menu")

        operation = input("Choose an operation: ")
        if operation == "1":
            print("Basic string properties")
            print(f"Length of the string: {len(demo_string)}")
            print(f"Contactination: {demo_string + ' is great!'}")
            print(f"Reputation: {demo_string * 3}")
        elif operation == "2":
            print("Case manipulation")
            print(f"String in uppercase: {demo_string.upper()}")
            print(f"String in lowercase: {demo_string.lower()}")
            print(f"String with all words capitalized: {demo_string.title()}")
            print(f"String with swaped case: {demo_string.swapcase()}")
        elif operation == "3":
            print("Searching operations")
            search_string = input("Enter a substring to search: ")
            if search_string in demo_string:
                print(f"'{search_string}' found in the string.")
                print(f"First occurrence (find): {demo_string.find(search_string)}")
                print(f"First occurrence (index): {demo_string.index(search_string)}")
                print(f"Count of occurrences: {demo_string.count(search_string)}")
                print(f"Starts with '{search_string}': {demo_string.startswith(search_string)}")
                print(f"Ends with '{search_string}': {demo_string.endswith(search_string)}")
            else:
                print(f"'{search_string}' not found in the string.")
        elif operation == "4":
            print("Slicing operations")
            print(f"Sliced string: {demo_string[:6]}")
        elif operation == "5":
            print("Split and join operations")
            split_string = demo_string.split()
            print(f"Split string: {split_string}")
            join_string = " ".join(split_string)
            print(f"Joined string: {join_string}")
        elif operation == "6":
            print("Whitespace handling")
            print(f"String with leading/trailing whitespace removed: '{demo_string.strip()}'")
            print(f"String with leading whitespace removed: '{demo_string.lstrip()}'")
            print(f"String with trailing whitespace removed: '{demo_string.rstrip()}'")
        elif operation == "7":
            print("Character replacement")
            old_char = input("Enter character to replace: ")
            new_char = input("Enter new character: ")
            print(f"String after replacement: {demo_string.replace(old_char, new_char)}")
        elif operation == "8":
            print("String alignment")
            print(f"Left aligned: '{demo_string.ljust(50)}'")
            print(f"Right aligned: '{demo_string.rjust(50)}'")
            print(f"Center aligned: '{demo_string.center(50)}'")
        elif operation == "9":
            print("String validation")
            print(f"Is alphanumeric: {demo_string.isalnum()}")
            print(f"Is alphabetic: {demo_string.isalpha()}")
            print(f"Is numeric: {demo_string.isnumeric()}")
        elif operation == "10":
            print("Formatting techniques")
            name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            print(f"Formatted string: My name is {name} and I am {age} years old." .format(name=name, age=age))
        elif operation == "11":
            print("Returning to main menu...")
            continue
    elif option == "3":
        print("Exiting...")
        menu = False
    else:
        print("Invalid option. Please try again.") 