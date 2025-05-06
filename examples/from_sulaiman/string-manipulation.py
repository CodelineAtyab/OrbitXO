from string import Template

app_running = True
while app_running:
    main_menu_input = input("""Main Menu:
1. Demonstration Mode
2. Challenge Mode
3. Exit
                            
Choose and Option: """)

    if main_menu_input == "1":
        sample_string = input("""DEMONSTRATION MODE
Enter a sample string: """)
        
        operation_running = True
        while operation_running:
            operation = input("""\nSelect operation:
1. Basic string properties
2. Case manipulation
3. Searching operations
4. Slicing operations
5. Split and join operations
6. Whitespace handling
7. Character replacement and translation
8. String alignment
9. String validation
10. Formatting techniques
11. Return to main menu
Choose an operation: """)
            while operation not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]:
                operation = input("Wrong buddy, I want an operation number, 1-11, no less no more: ")
            if operation == "1":
                print("\nBasic string properties:")
                print("Length: " + str(len(sample_string)) + " Characters")
                print("Concatination: " + sample_string + "And fun too! Good for easy string manipulation")
                print("Repetition:" + ("\n" + sample_string)* 3)
            elif operation == "2":
                print("\nCase manipulation:")
                print("Upper Case: " + sample_string.upper())
                print("Lower Caes: " + sample_string.lower())
                print("Title: " + sample_string.title())
                print("Swap Case: " + sample_string.swapcase())
            elif operation == "3":
                print("\nFinding Python:")
                find_string = sample_string.find("Python")
                if find_string == -1:
                    print("nowhere to be found")
                else:
                    print(str(find_string))
                print("\nPython Index: " + str(sample_string.index("Python")) + "\n")
                print("Python Count: " + str(sample_string.count("Python")) + "\n")
                print("String Start's with Python: " + str(sample_string.startswith("Python")))
                print("And End's with learn!: " + str(sample_string.endswith("learn!")))
            elif operation == "4":
                print("\nSlicing operations:")
                print("First 6 Characters: " + sample_string[:6])
                print("Last 6 Characters: " + sample_string[-6:])
                print("Every Second Character: " + sample_string[::2])
                print("Reverse: " + sample_string[::-1])
                print('Extract "powerful": ' + sample_string[10:18])
            elif operation == "5":
                print("\nSplit and Join operations: ")
                seperator = " "
                string_split = sample_string.split(seperator)
                print("Split: " + str(string_split))
                print("Join: " + seperator.join(string_split))
            elif operation == "6":
                print("\nWhitespace Handling:")
                string_split = sample_string.split(" ")
                sample_whitespaced_word = "    " + string_split[2] + "    "
                sample_whitespaced_string = " ".join(string_split[0:2]) + sample_whitespaced_word + " ".join(string_split[3:len(string_split)])
                print(sample_whitespaced_string)
                sample_whitespaced_string = " ".join(string_split[0:2]) + sample_whitespaced_word.strip() + " ".join(string_split[3:len(string_split)])
                print("Strip: " + sample_whitespaced_string)
                sample_whitespaced_string = " ".join(string_split[0:2]) + sample_whitespaced_word.lstrip() + " ".join(string_split[3:len(string_split)])
                print("Left Strip: " + sample_whitespaced_string)
                sample_whitespaced_string = " ".join(string_split[0:2]) + sample_whitespaced_word.rstrip() + " ".join(string_split[3:len(string_split)])
                print("Right Strip: " + sample_whitespaced_string)
            elif operation == "7":
                print("\nCharacter Replacement and Translation:")
                print("Repleacement: " + sample_string.replace("Python", "Java"))
                print("Translation: " + sample_string.translate(str.maketrans("aeiou", "12345")))
            elif operation == "8":
                print("\nString Alignment and Padding:")
                print("Center:\n" + sample_string.center(len(sample_string) *2) + "And fun too! Good for easy string manipulation")
                print("Left Justified:\n" + sample_string.ljust(len(sample_string) *2) + "And fun too! Good for easy string manipulation")
                print("Right Justified:\n" + sample_string.rjust(len(sample_string) *2) + "And fun too! Good for easy string manipulation")
            elif operation == "9":
                print("\nString Validation:")
                print(sample_string)
                print("Is it Alphanumeric?:" + str(sample_string.isalnum()))
                print("Is it Alphabetic?:" + str(sample_string.isalpha()))
                print("are there ASCII characters?:" + str(sample_string.isascii()))
                print("Is it Decimal?:" + str(sample_string.isdecimal()))
                print("Is it a Digit?:" + str(sample_string.isdigit()))
                print("Is it an Identifier?:" + str(sample_string.isidentifier()))
                print("Is it all in Lower Case?:" + str(sample_string.islower()))
                print("Is it Numeric?:" + str(sample_string.isnumeric()))
                print("Is it Printable?:" + str(sample_string.isprintable()))
                print("Is it just White Spaces?:" + str(sample_string.isspace()))
                print("Is it Title Case?:" + str(sample_string.istitle()))
                print("Is it  all in Upper Case?:" + str(sample_string.isupper()))
            elif operation == "10":
                print("\nFormatting Techniques:")
                extra_string = "This statement '{}' is genius"
                print(extra_string.format(sample_string))
                print(f"This statement '{sample_string}' is genius")
                print("This statment '%s' is genius" %(sample_string))
                template = Template("This statment '$s' is genius")
                print(template.substitute(s=sample_string))
            elif operation == "11":
                operation_running = False
    elif main_menu_input == "2":
        print("Challenge Mode\n")
    elif main_menu_input == "3":
        app_running = False
    else:
        print("invalid input, choose again\n")