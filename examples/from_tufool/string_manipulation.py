running_menu = True
while running_menu:
    print("Main Menu:\n1. Demonstration Mode\n2. Exit")
    option = input("Choose an option: ")
    if option == "1":
        print("DEMONSTRATION MODE")
        demonstration_string = input("Enter a sample string: Python is powerful and easy to learn! ")
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
        operation = input("Choose an operation between 1 to 11: ")
        if operation == "1":
            print("Basic string operations")
            print(f"Length of the string: {len(demonstration_string)}")
            print(f"Concatenation: {demonstration_string + ' is great!'}")
            print(f"Repitition: {demonstration_string * 3}")
        elif operation == "2":
            print("Case manipulation")
            print(f"String in uppercase: {demonstration_string.upper()}")
            print(f"String in lowercase: {demonstration_string.lower()}")
            print(f"String with all words capitalized: {demonstration_string.title()}")
            print(f"String with swaped case: {demonstration_string.swapcase()}")
            
        elif operation == "3":
            print("String searching operations")
            searching_string = input("Enter a sub-string to search: ")
            if searching_string in demonstration_string:
                print(f"'{searching_string}' found in the string.")
                print(f"First string (find): {demonstration_string.find(searching_string)}")
                print(f"First string (index): {demonstration_string.index(searching_string)}")
                print(f"Count of strings: {demonstration_string.count(searching_string)}")
                print(f"Starts with '{searching_string}': {demonstration_string.startswith(searching_string)}")
                print(f"Ends with '{searching_string}': {demonstration_string.endswith(searching_string)}")
            else:
                print(f"'{searching_string}' not found in the string.")
        elif operation == "4":
            print("Slicing operations")
            print(f"Sliced string: {demonstration_string[:6]}")
        elif operation == "5":
            print("Split and join operations")
            split_string = demonstration_string.split()
            print(f"Split string: {split_string}")
            join_string = " ".join(split_string)
            print(f"Joined string: {join_string}")
        elif operation == "6":
            print("Whitespace handling")
            print(f"String with leading/trailing whitespace removed: '{demonstration_string.strip()}'")
            print(f"String with leading whitespace removed: '{demonstration_string.lstrip()}'")
            print(f"String with trailing whitespace removed: '{demonstration_string.rstrip()}'")
        elif operation == "7":
            print("Character replacement & translation")
            old_char = input("Enter character to replace: ")
            new_char = input("Enter new character: ")
            print(f"String after replacement: {demonstration_string.replace(old_char, new_char)}")
            english_char = input("Enter character to translate: ")
            translated_char = input("Enter character to replace it with in translation: ")
            print(f"String after translation: {demonstration_string.translate(english_char)}")
        elif operation == "8":
            print("String alignment")
            print(f"Left aligned: '{demonstration_string.ljust(50)}'")
            print(f"Right aligned: '{demonstration_string.rjust(50)}'")
            print(f"Center aligned: '{demonstration_string.center(50)}'")
        elif operation == "9":
            print("String validation")
            print(f"Is alphanumeric: {demonstration_string.isalnum()}")
            print(f"Is alphabetic: {demonstration_string.isalpha()}")
            print(f"Is numeric: {demonstration_string.isnumeric()}")
        elif operation == "10":
            print("Formatting techniques")
            name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            print(f"Formatted string: My name is {name} and I am {age} years old." .format(name=name, age=age))
        elif operation == "11":
            print("Returning to main menu...")
            continue
    elif option == "2":
        print("Exiting...")
        running_menu = False
    else:
        print("Invalid option. Please try again.")