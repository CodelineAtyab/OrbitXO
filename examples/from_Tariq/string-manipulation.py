print("Main Menu:")
print("1. Demonstration Mode")
print("2. Challenge Mode")
print("3. Exit")
x= input("Choose an option: ")

menu= True
while menu:

    if x == '1':
        print("You have selected Demonstration Mode.")
        print("DEMONSTRATION MODE")
        sample = input("Enter a sample string: ")
        print("Select operation: ")
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

        d= input("Choose an operation: ")
        if d == '1':
            print("Basic string properties: ")
            print("1. Length of the string: ")
            print("Length of the string: ", len(sample))
            print("2. concatenation: ")
            print("Concatenation: ", sample + " is a string")
            print("3. repetition: ")
            print("Repetition: ", sample * 3)
        elif d == '2':
            print("Case manipulation: ")
            print("1. Uppercase: ")
            print("Uppercase: ", sample.upper())
            print("2. Lowercase: ")
            print("Lowercase: ", sample.lower())
            print("3. Title case: ")
            print("Title case: ", sample.title())
            print("4. Swap case: ")
            print("Swap case: ", sample.swapcase())
        elif d == '3':
            search = input("Searching operations what are you looking for: ")
            print("1. Find: ")
            print("Find: ", sample.find(search))
            print("2. Index: ")
            print("Index: ", sample.index(search))
            print("3. Count: ")
            print("Count: ", sample.count(search))
            print("4. Starts with: ")
            print("Starts with: ", sample.startswith(search))
            print("5. Ends with: ")
            print("Ends with: ", sample.endswith(search))
        elif d == '4':
            print("Slicing operations ")
            print("1. Slicing: ")
            print("Slicing: ", sample[2:5])
            print("2. extraction : ")
            print("Extraction: ", sample[0:5:2])
        elif d == '5':
            print("Split and join operations: ")
            print("1. Split: ")
            print("Split: ", sample.split())
            print("2. Join: ")
            print("Join: ", "8".join(sample))
            print("partation: ", sample.partition("a"))
        elif d == '6':
            print("Whitespace handling: ")
            print("1. Strip: ")
            print("Strip: ", sample.strip())
            print("2. Lstrip: ")
            print("Lstrip: ", sample.lstrip())
            print("3. Rstrip: ")
            print("Rstrip: ", sample.rstrip())
        elif d == '7':
            print("Character replacement: ")
            print("1. Replace: ")
            print("Replace: ", sample.replace("a", "b"))
            print("2. Translate : ")
            print("Translate: ", sample.translate(str.maketrans("a", "b")))
        elif d == '8':
            print("String alignment: ")
            print("1. Center: ")
            print("Center: ", sample.center(20, "*"))
            print("2. Ljust: ")
            print("Ljust: ", sample.ljust(20, "*"))
            print("3. Rjust: ")
            print("Rjust: ", sample.rjust(20, "*"))
        elif d == '9':
            print("String validation: ")
            print("1. Is alpha: ")
            print("Is alpha: ", sample.isalpha())
            print("2. Is digit: ")
            print("Is digit: ", sample.isdigit())
            print("3. Is alnum: ")
            print("Is alnum: ", sample.isalnum())
            print("4. Is space: ")
            print("Is space: ", sample.isspace())
        elif d == '10':
            print("Formatting techniques: ")
            print("1. Format: ")
            print("Format: ", "Hello {}".format(sample))
            print("2. F-string: ")
            print("F-string: ", f"Hello {sample}")
        elif d == '11':
            menu = True
            break
    elif x == '2':
        print("You have selected Challenge Mode.")
        print("CHALLENGE MODE")
        sentence = input("Please write a sentence: ")
        char = int(input("Write the amount of characters. The program will search for words with more than the amount you picked: "))
        print("I will list the words with more than", char, "characters:")
        words = sentence.split()
        matched_words = []
        for word in words:
         print(f"Checking word: {word}")
         if len(word) > char:
            matched_words.append(word)
        if matched_words:
            print("Words with more than", char, "characters:")
            for word in matched_words:
                print(word)
          


                
        menu = True
        break

    
    elif x== '3':
        print("You have selected Exit.")
        menu = False
        break
    else:
        print("Invalid option. Please try again.")
       


        
      



            
            

            
        
        
