print("Welcome to the String Manipulation Tool!")
while True:
    print("1. Demonstration Mode")
    print("2. Challenge Mode")
    print("3. Exit")

    choice = input("Choose an option (1-3): ")
      
    if choice == "1":
        print("\nDEMONSTRATION MODE")
        sample_string: str = input("Enter a sample string: ")

        while True:
            print("\nSelect operation:")
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

            demo_choice = input("Choose an operation (1-11): ") 

            if demo_choice == "1":
                print("\nBasic String Properties:")
                print("Length:", len(sample_string))
                print("Concatenation:", sample_string + " And have fun too")
                print("Repetition:", sample_string.split()[0] * 3) 

            elif demo_choice == "2":
                print("\nCase Manipulation:")
                print("Upper:", sample_string.upper())
                print("Lower:", sample_string.lower())
                print("Title:", sample_string.title()) 


            elif demo_choice == "3":
                word = input("Enter a word to search: ")
                print("\nSearching Operations:")
                print("Find:", sample_string.find(word))
                print("Count:", sample_string.count(word))
                print("Starts with it?", sample_string.startswith(word))   


            elif demo_choice == "4":
                print("\nSlicing Operations:")
                print("First 5 letters:", sample_string[:5])
                print("Last 4 letters:", sample_string[-4:])
                print("Every 2nd letter:", sample_string[::2])
                print("Reversed string:", sample_string[::-1])

            elif demo_choice == "5":
                print("\nSplit and Join:")
                words = sample_string.split()
                print("Split into list:", words)
                print("Join with dashes:", "-".join(words))

            elif demo_choice == "6":
                print("\nWhitespace Handling:")
                spaced = "   " + sample_string + "   "
                print("Original with spaces:", repr(spaced))
                print("without spaces:", spaced.strip()) 
                
            elif demo_choice == "7":
                print("\nCharacter Replacement:")
                print("Replace 'e' with '*':", sample_string.replace("e", "*"))
                table = str.maketrans("aeiou", "12345")
                print("Translate vowels to numbers:", sample_string.translate(table))

            elif demo_choice == "8":
                print("\nString Alignment:")
                print("Center (width 30):", sample_string.center(30, "-"))
                print("Left justify:", sample_string.ljust(30, "*"))
                print("Right justify:", sample_string.rjust(30, "."))    

            elif demo_choice == "9":
                print("\nString Validation:")
                print("Letters Only", sample_string.isalpha())
                print("Numbers Only", sample_string.isdigit())
                print("Spaces Only", sample_string.isspace())    
    
            elif demo_choice == "10":
                print("\nFormatting Techniques:")
                print("F-string example:")
                print(f"Result: Python has {len('Python')} letters") 
                print("Percentage formatting:")
                print("%d%% of Python devs love strings" % 90) 
            
            elif demo_choice == "11":
                break

            else:
                print("Please enter a number between 1 and 11.") 



    elif choice == "2":
        print("\nCHALLENGE MODE")

        print("\nChallenge 1:")
        print("Reverse this string: 'Python is fun'")
        answer1 = input("Your code or 'hint': ")

        if answer1 == "hint":
            print("Hint: Use [::-1]") 

        elif answer1 == 'nuf si nohtyP':
            print("Correct! ") 
        else:
            print("Incorrect. A correct answer is: 'nuf si nohtyP'")
            print(' Use the code "Python is fun"[::-1]')  


        print("\nChallenge 2:")
        print("Replace every 'e' in 'Elephants eat everything' with '*'")
        answer2 = input("Your code or 'hint': ") 


        if answer2 == "hint":
            print("Hint: .replace("", "*").replace("", "*")") 

        elif answer2 == '*l*phants *at *v*rything':
           print("Correct!")

        else:
            print("Incorrect. A correct answer is: *l*phants *at *v*rything")
            print('Using the code "Elephants eat everything".replace("e", "*").replace("E", "*")')



    elif choice == "3":
        print("Thanks for using String Manipulation Tool Goodbye")
        break

    else:
        print("Please enter a number from 1 to 3.")            
 