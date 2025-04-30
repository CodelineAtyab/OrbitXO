menu = True
while menu:
    print("Main Menu:")
    print("1. Demonstration Mode")
    print("2. Exit")

    a = input("Choose an option: ")
    x = True
    if a == "1":
        while x:
        
            print("DEMONSTRATION MODE")
            stringsample = str(input("Enter a sample string: "))
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
                print(f"\nLength: {len(stringsample)} characters")
                print("Concatenation:")
                print(stringsample + " It's enjoyable and simplifies string handling.")
                print("Hint: +")
                print("Repetition:")
                print("Python" * 5)
                print("Hint: 'Python' * 4")
            elif option == "2":
                print("\nUppercase:", stringsample.upper())
                print("Lowercase:", stringsample.lower())
                print("Title Case:", stringsample.title())
                print("Swapcase:", stringsample.swapcase())
            elif option == "3":
                print("\nFind 'easy':", stringsample.find("easy"))
                print("Index of 'powerful':", stringsample.index("powerful"))
                print("Count of 'a':", stringsample.count("a"))
                print("Starts with 'Python':", stringsample.startswith("Python"))
                print("Ends with '!':", stringsample.endswith("!"))
            elif option == "4":
                print("\nFirst 6 characters:", stringsample[:6])
                print("Code: sample_string[:6]")
                print("Last 6 characters:", stringsample[-6:])
                print("Code: sample_string[-6:]")
                print("Every other character:", stringsample[::2])
                print("Code: sample_string[::2]")
                print("Reverse string:", stringsample[::-1])
                print("Code: sample_string[::-1]")
                print("Extract 'powerful':", stringsample[10:18])
                print("Code: sample_string[10:18]")
            elif option == "5":
                split_words = stringsample.split()
                print("\nSplit into list:", split_words)
                print("Join with dash:", "-".join(split_words))
                before, middle, after = stringsample.partition("easy")
                print("Partition on 'easy':")
                print("Before:", before)
                print("Middle:", middle)
                print("After:", after)
            elif option == "6":
                messy = "   Hello Aiman!   "
                print("\nOriginal string:", repr(messy))
                print("strip():", messy.strip())
                print("lstrip():", messy.lstrip())
                print("rstrip():", messy.rstrip())
            elif option == "7":
                print("\nReplace 'easy' with 'simple':", stringsample.replace("easy", "simple"))
                table = str.maketrans("aeiou", "12345")
                print("Translate vowels to numbers:", stringsample.translate(table))
            elif option == "8":
                print("\nCentered (width 40):", stringsample.center(40, "*"))
                print("Left Justified:", stringsample.ljust(40, "-"))
                print("Right Justified:", stringsample.rjust(40, "-"))
            elif option == "9":
                print("\nIs alphabetic:", stringsample.replace(" ", "").isalpha())
                print("Is digit:", stringsample.isdigit())
                print("Is alphanumeric:", stringsample.replace(" ", "").isalnum())
                print("Is lowercase:", stringsample.islower())
                print("Is uppercase:", stringsample.isupper())
            elif option == "10":
                word = "Python"
                date = "2025-04-27"
                percent = 90
                print(f"\nUsing f-string: {word} has {len(word)} letters and is used by many developers")
                print("Using .format():", "Hello, {}! Today is {}".format("Team Code Orbit", date))
                print("Using % operator:", "%d%% of Python developers love string manipulation" % percent)
            elif option == "11":
                x = False
    else:
        menu = False