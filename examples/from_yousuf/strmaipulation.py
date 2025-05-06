running_menu = True
while running_menu:
    print("\nMain Menu:\n1. Demonstration Mode\n2. Exit")
    option = input("Choose an option: ")
    if option == "1":
        print("\nDEMONSTRATION MODE")
        demonstration_string = input("Enter a sample string: ")
        whitespace_string = "   " + demonstration_string + "   "
        while True:
            print("\nSelect operation:\n" \
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
                print("\nBasic String Properties:")
                print(f"Length: {len(demonstration_string)} characters")
                print("Concatenation:\nResult:", demonstration_string + " And fun too! Good for easy string manipulation")
                print("Repetition:\nResult:", demonstration_string * 3)
            elif operation == "2":
                print("\nCase Manipulation:")
                print("Uppercase:", demonstration_string.upper())
                print("Lowercase:", demonstration_string.lower())
                print("Title Case:", demonstration_string.title())
                print("Swap Case:", demonstration_string.swapcase())
            elif operation == "3":
                print("\nSearching Operations:")
                searching_string = input("Enter a sub-string to search: ")
                if searching_string in demonstration_string:
                    print(f"'{searching_string}' found in the string.")
                    print(f"Find string (find): {demonstration_string.find(searching_string)}")
                    print(f"First index (index): {demonstration_string.index(searching_string)}")
                    print(f"Count of occurrences: {demonstration_string.count(searching_string)}")
                    print(f"Starts with '{searching_string}': {demonstration_string.startswith(searching_string)}")
                    print(f"Ends with '{searching_string}': {demonstration_string.endswith(searching_string)}")
                else:
                    print(f"'{searching_string}' not found in the string.")
            elif operation == "4":
                print("\nSlicing Operations:")
                print(f"First 6 characters: {demonstration_string[:6]}")
                print(f"Last 6 characters: {demonstration_string[-6:]}")
                print(f"Every other character: {demonstration_string[::2]}")
                print(f"Reverse string: {demonstration_string[::-1]}")
                print(f"Extract 'powerful': {demonstration_string[10:18]}")
            elif operation == "5":
                print("\nSplit and Join Operations:")
                split_string = demonstration_string.split()
                print("Split string:", split_string)
                joined_string = " ".join(split_string)
                print("Joined string:", joined_string)
            elif operation == "6":
                print("\nWhitespace Handling:")
                print(f"Original with whitespaces: '{whitespace_string}'")
                print(f"Using strip(): '{whitespace_string.strip()}'")
                print(f"Using lstrip(): '{whitespace_string.lstrip()}'")
                print(f"Using rstrip(): '{whitespace_string.rstrip()}'")
            elif operation == "7":
                print("\nCharacter Replacement & Translation:")
                old_char = input("Enter character to replace: ")
                new_char = input("Enter new character: ")
                if old_char in demonstration_string:
                    print("String after replacement:", demonstration_string.replace(old_char, new_char))
                else:
                    print(f"Character '{old_char}' not found in the string. No replacement done.")
                english_char = input("Enter character to translate: ")
                translated_char = input("Enter character to replace it with in translation: ")
                translation_table = str.maketrans(english_char, translated_char)
                print("String after translation:", demonstration_string.translate(translation_table))
            elif operation == "8":
                print("\nString Alignment:")
                print("Left aligned:", demonstration_string.ljust(50))
                print("Right aligned:", demonstration_string.rjust(50))
                print("Center aligned:", demonstration_string.center(50))
            elif operation == "9":
                print("\nString Validation:")
                print("Is alphanumeric:", demonstration_string.isalnum())
                print("Is alphabetic:", demonstration_string.isalpha())
                print("Is numeric:", demonstration_string.isnumeric())
            elif operation == "10":
                print("\nFormatting Techniques:")
                print("Using f-string:")
                print(f"{'Python'} has {len('Python')} letters and is used by many developers")
                print("Using .format():")
                print("Hello, {name}! Today is {date}".format(name="Team Code Orbit", date="2025-04-27"))
                print("Using % operator:")
                print("%d%% of Python developers love string manipulation" % 90)
            elif operation == "11":
                print("Returning to main menu...")
                # The `continue` statement skips to the next iteration of the while loop (back to main menu)
                break
            else:
                print("Invalid operation. Please try again.")
    elif option == "2":
        print("Exiting...")
        running_menu = False
    else:
        print("Invalid option. Please try again.")
