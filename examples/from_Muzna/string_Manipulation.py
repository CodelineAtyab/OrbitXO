while True:
    print("Main Menu:\n 1. Demonstration Mode \n 2. Challenge Mode \n 3. Exit")

    option1 = int(input("Choose an option (1-3): "))

    if option1 == 1:
        while True:
            print("\nDEMONSTRATION MODE")
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
            print("11. Return to main menu\n")

            option2 = int(input("Choose an operation: "))  # Submenu choice
            if option2 == 11:
                break  # Return to main menu
            

            text = input("Enter a sample string: ")  # Ask for input string

            if option2 == 1:
                print("\nBasic operations:")
                print(f"\nLength: {len(text)}")  # String length
                text2 = input("Enter a text to add:")  # String concatenation
                print(f"Result: {text + text2}")
                first_word = text.split()[0]  # Repeat the first word 3 times
                print(f"Repetition: {first_word * 3}")

            elif option2 == 2:
                print("\nCase manipulation:")
                print(f"Upper: {text.upper()}")
                print(f"Lower: {text.lower()}")
                print(f"Title: {text.title()}")
                print(f"Swapcase: {text.swapcase()}")

            elif option2 == 3:
                print("\nString searching:")
                txt_find = input("What do you want to find in the text: ")
                print(f"Find '{txt_find}': {text.find(txt_find)}")  # Find index
                start_with = input("Find text start with: ")
                print(f"Count '{start_with}': {text.count(start_with)}")  # Count
                end_with = input("Find text end with: ")
                print(f"Starts with '{end_with}': {text.startswith(end_with)}")  # Startswith check

            elif option2 == 4:
                print("\nSlicing Operations:")
                print(f"First 6 characters: {text[0:6]}")
                print(f"Last 6 characters: {text[-6:]}")
                print(f"Every other character: {text[::2]}")
                print(f"Reverse string: {text[::-1]}")

            elif option2 == 5:
                print("\nString splitting, joining and partition operations")
                print(f"Split the words: {text.split()}")
                words = input("Enter a word to split by: ")
                print(f"Split by '{words}': {text.partition(words)}")
                print(f"Join with '-': {'-'.join(text)}")

            elif option2 == 6:
                print("\nWhitespace handling")
                print(f"Remove whitespace: {text.strip()}")
                print(f"Remove left whitespace: {text.lstrip()}")
                print(f"Remove right whitespace: {text.rstrip()}")

            elif option2 == 7:
                print("\nCharacter replacement and translation")
                print(f"Replace 'a' with '@': {text.replace('a', '@')}")
                tran = str.maketrans("aeiou", "AEIOU")
                print(f"Translate vowels: {text.translate(tran)}")

            elif option2 == 8:
                print("\nString alignment and padding")
                print("Center:", text.center(20, "-"))
                print("Left Justify:", text.ljust(20, "*"))
                print("Right Justify:", text.rjust(20, "*"))

            elif option2 == 9:
                print("\nString validation methods")
                print("Is Alpha:", text.isalpha())
                print("Is Digit:", text.isdigit())
                print("Is Alnum:", text.isalnum())
                print("Is Title:", text.istitle())

            elif option2 == 10:
                print("\nString formatting techniques")
                text3 = "Python"
                print(f"{text3} has {len(text3)} letters and is used by many developers")
                print("Using .format():")
                print("Hello, {team_name}! Today is {date}".format(team_name="Team Code Orbit", date="2025-05-01"))
                print(r"Using % operator:")
                print("%d%% of Python developers love string manipulation" % 90)

            else:
                print("Enter a number between 1-11")
                break
                


    elif option1==2:
        print("CHALLENGE MODE")
        sentence:str =input("enter a sentence : ")
        words = sentence.split() 
        count = 0
        for w in words:
            if len(w) > 3:  
                count += 1  
        print("Number of words with more than 3 letters:", count)
            
        text = "hello world"
        words2 = text.split()               
        capitlWords = []            

        for word in words2:
            capitlWords.append(word.capitalize())

        # Join the words with a dash
        result = "-".join(capitlWords)
        print(result)  
      
    elif option1 == 3:
        print("Exit!!")
        break

    

