def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Demonstration Mode")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            demonstration_mode()
        elif choice == "2":
            print("Goodbye, Yousuf!")
            break
        else:
            print("Please enter 1 or 2.")

def demonstration_mode():
    sample_string = input("\nEnter a sample string: ")

    while True:
        print("\nDEMONSTRATION MODE")
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

        option = input("Choose an operation: ")

        if option == "1":
            print(f"\nLength: {len(sample_string)} characters")
            print("Concatenation:")
            print(sample_string + " And fun too! Good for easy string manipulation")     
            print("Repetition:")
            print("Python" * 3)
            print(" 'Python' * 3")

        elif option == "2":
            print("\nUppercase:", sample_string.upper())
            print("Lowercase:", sample_string.lower())
            print("Title Case:", sample_string.title())
            print("Swapcase:", sample_string.swapcase())

        elif option == "3":
            print("\nFind 'easy':", sample_string.find("easy"))
            print("Index of 'powerful':", sample_string.index("powerful"))
            print("Count of 'a':", sample_string.count("a"))
            print("Starts with 'Python':", sample_string.startswith("Python"))
            print("Ends with '!':", sample_string.endswith("!"))

        elif option == "4":
            print("\nFirst 6 characters:", sample_string[:6])
            print("Code: sample_string[:6]")
            print("Last 6 characters:", sample_string[-6:])
            print("Code: sample_string[-6:]")
            print("Every other character:", sample_string[::2])
            print("Code: sample_string[::2]")
            print("Reverse string:", sample_string[::-1])
            print("Code: sample_string[::-1]")
            print("Extract 'powerful':", sample_string[10:18])
            print("Code: sample_string[10:18]")

        elif option == "5":
            split_words = sample_string.split()
            print("\nSplit into list:", split_words)
            print("Join with dash:", "-".join(split_words))
            before, middle, after = sample_string.partition("easy")
            print("Partition on 'easy':")
            print("Before:", before)
            print("Middle:", middle)
            print("After:", after)

        elif option == "6":
            messy = "   Hello Yousuf!   "
            print("\nOriginal string:", repr(messy))
            print("strip():", messy.strip())
            print("lstrip():", messy.lstrip())
            print("rstrip():", messy.rstrip())

        elif option == "7":
            print("\nReplace 'easy' with 'simple':", sample_string.replace("easy", "simple"))
            table = str.maketrans("aeiou", "12345")
            print("Translate vowels to numbers:", sample_string.translate(table))

        elif option == "8":
            print("\nCentered (width 40):", sample_string.center(40, "*"))
            print("Left Justified:", sample_string.ljust(40, "-"))
            print("Right Justified:", sample_string.rjust(40, "-"))

        elif option == "9":
            print("\nIs alphabetic:", sample_string.replace(" ", "").isalpha())
            print("Is digit:", sample_string.isdigit())
            print("Is alphanumeric:", sample_string.replace(" ", "").isalnum())
            print("Is lowercase:", sample_string.islower())
            print("Is uppercase:", sample_string.isupper())

        elif option == "10":
            word = "Python"
            date = "2025-04-27"
            percent = 90
            print(f"\nUsing f-string: {word} has {len(word)} letters and is used by many developers")
            print("Using .format():", "Hello, {}! Today is {}".format("Team Code Orbit", date))
            print("Using % operator:", "%d%% of Python developers love string manipulation" % percent)

        elif option == "11":
            break
        else:
            print("Please choose a valid number (1 to 11)")



main_menu()