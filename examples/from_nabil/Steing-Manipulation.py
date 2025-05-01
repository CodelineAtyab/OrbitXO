while True:
    print("main menu")
    print("1. Demonstration Mode")
    print("2. Exit")

    x = input("Choose an option: ")

    main_menu = True
    while main_menu: 
        if x == "1":
            print("DEMONSTATION MODE")
            sample_string = str(input("give me a word: "))
            print("Select operation")
            print("1. Basic string properties")
            print("2. Case manipulation")
            print("3. Seaeching operations")
            print("4. Slicing operations")
            print("5. Split and join operations")
            print("6. Whitespace handling")
            print("7. Character replacement")
            print("8. String alignment")
            print("9. String validation")
            print("10. Formatting techniques")
            print("11. Return to main menu")
            select_operation = input("choose an operation: ")
            if select_operation == "1":
                print("Basic String Properties: ")
                print("lenth: " + str(len(sample_string)))
                print("concatenation")
                print("result: " + sample_string + "is a string")
                print("Repetition")
                print("result: " + sample_string * 2)
            elif select_operation == "2":
                print("Case manipulation: ")
                print(sample_string.upper())
                print(sample_string.lower())
                print(sample_string.title())
                print(sample_string.swapcase())
            elif select_operation == "3":
                print("String searching: ")
                print(sample_string.find("a"))
                print(sample_string.index("a"))
                print(sample_string.count("a"))
                print(sample_string.startswith("a"))
                print(sample_string.endswith("b"))
            elif select_operation == "4":
                print("slicing and extraction")
                print("slicing: " , sample_string[1:4])
                print("extraction: " , sample_string[2:4:5])
            elif select_operation == "5":
                print("splitting & joining operations")
                print("splitting: ",sample_string.split("a"))
                print("joining: " , "5".join(sample_string))
                print("partitioning: ", sample_string.partition("a"))
            elif select_operation == "6":
                print("whitespace handling")
                print("strip: ", sample_string.split())
                print("lstrip: ", sample_string.lstrip())
                print("rstrip: ", sample_string.rstrip())
            elif select_operation == "7":
                print("chgaracter replacement & translation")
                print("replacement: ", sample_string.replace('hello','but').replace('why','no'))
                print("translation: ", sample_string.translate(str.maketrans("a","b")))
            elif select_operation == "8":
                print("alignment and padding")
                print(sample_string.center(25))
                print(sample_string.ljust(20))
                print(sample_string.rjust(15))
            elif select_operation == "9":
                print("validation methods")
                print(sample_string.isalpha())
                print(sample_string.isdigit())
            elif select_operation == "10":
                print("formatting techniques")
                name = input("enter your name ")
                age = int(input("enter your age:"))
                print(f"my name is {name} and I am {age} years old.".format(name, age))
            elif select_operation == "11":
                main_menu = False

        elif x == "2":
            False