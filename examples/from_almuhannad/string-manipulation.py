print("Main menu: ")
print("1. demonstration Mode")
print("2. Challenge Mode")
print("3. Exit")

a = input("Choose an option : ")

menu = True
while menu:
    if a == "1":
        print("DEMONSTRATION MODE")
        samplestring = str(input("Enter a sample string: "))
        print("Select Operation: ")
        print("1. Basic string properties")
        print("2. Case manipulation")
        print("3. Searching operations")
        print("4. Slicing operations")
        print("5. Split and join operations")
        print("6. Whitespace handling")
        print("7. Character replacement")
        print("8. string alignment")
        print("9. string validation")
        print("10. Formatting techniques")
        print("11. Return to main menu")
        select_op = input("Select Operation: ")
        if select_op == "1":
            print("Basic String Properties:")
            print("Lenth: " + str(len(samplestring)) + " "  + "Characters")

            print("Conatention:")
            print("result : " + samplestring + " is a string")

            print("Reputition:")
            print("result: " + samplestring * 4 )
        
        elif select_op == "2":
            print("Case Manipulation:")
            print(samplestring.upper())
            print(samplestring.lower())
            print(samplestring.swapcase())
        
        elif select_op == "3":
            print("String Searching :")
            print(samplestring.find("a"))
            print(samplestring.index("a"))
            print(samplestring.count("a"))
            print(samplestring.startswith("a"))
            print(samplestring.endswith("b"))
        
        elif select_op == "4":
            print("Slicing and Extraction: ")
            print("Slicing: ", samplestring[2:5])
            print("extraction: ", samplestring[2:4:5])

        elif select_op == "5":
            print("splitting: ", samplestring.split())
            print("joining: " , " 9 " .join(samplestring))
            print("Partioning: ", samplestring.partition("a"))

        elif select_op == "6":
            print("White handling: ")
            print("strip: ", samplestring.strip())
            print("lstrip: ", samplestring.lstrip())
            print("rstrip ", samplestring.rstrip())

        elif select_op == "7":
            print("Replace and Traslation: ")
            print("Replaceing: ", samplestring.replace('hello','but').replace('why','no'))
            print("Translation: ", samplestring.translate(str.maketrans("a","b")))

        elif select_op == "8":
            print("String alignment and padding: ")
            print(samplestring.center(20))
            print(samplestring.ljust(20))
            print(samplestring.rjust(10))
        
        elif select_op == "9":
            print("String validation methods (isalpha, isdigit, etc.): ")
            print(samplestring.isalpha())
            print(samplestring.isdigit())
        
        elif select_op == "10":
            print("Formatting techniques")
            name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            print(f"Formatted string: My name is {name} and I am {age} years old." .format(name=name, age=age))

        elif select_op == "11":
            menu = True