running  = True

while running:
    print("\nMain Menu:")
    print("1. Demonstration Mode")
    print("2. Challenge Mode")
    print("3. Exit")

    choose = input("Select one (1, 2, or 3): ").strip()

    if choose == "1":
        print("\nYou selected Demonstration Mode.")
        demo_running = True
        while demo_running:
            print("\nDemonstration Menu:")
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

            demo_choice = input("Select one (1-11): ").strip()

            if demo_choice == "1":
                print("You selcetd Basic string properties")
                Basic_string_properties = True 
                while Basic_string_properties:
                    print("1. lenght")
                    print("2. Concatenation ")
                    print("3. Repetition ")
                    print("4. return ")

                    Basic_string_propertie_choice = input("Select one (1-4): ").strip()
                        
                    if Basic_string_propertie_choice == "1":
                        print("You chose: lenght")
                        length_sen=input("enter a sentence:")
                        print(f"lenght result={len(length_sen)}character")#f (f string,number+text in one line )

                    elif Basic_string_propertie_choice == "2":
                        print("You chose: Concatenation")
                        Concatenation_sen =input("enter a sentence:")
                        Result_sen = Concatenation_sen+"I enjoy learning python"
                        print (Result_sen)

                    elif Basic_string_propertie_choice == "3":
                        print("You chose: Repetition")
                        rep_word= input("dublicate the word 3 times:")
                        print (rep_word*3)

                    elif Basic_string_propertie_choice == "4":
                        print("you chose: return ")
                        Basic_string_properties = False # when return before else 

                    else:
                        print("Invalid input. Please choose between 1 and 4.")

            elif demo_choice == "2":
                print("You chose: Case manipulation")         
                Case_Manipulation = True 
                while Case_Manipulation:
                    print("1.upper")
                    print("2.lower ")
                    print("3.title ")
                    print("4.swapcase")
                    print("5.return")
                    
                    Case_Manipulation = input("Select one (1-5): ").strip()
                    sentance= input ("enter a word: ") 
                    if Case_Manipulation== "1":
                            print("You chose:upper")
                            print (sentance.upper())# a must upper()to keep it capital .


                    elif Case_Manipulation== "2":
                            print("You chose:lower")
                            print (sentance.lower())# a must lower()to keep it low case  .

                    elif Case_Manipulation== "3":
                            print("You chose:title")
                            text = "hello world"
                            print(text.title())  # Output: "Hello World" 

                    elif Case_Manipulation== "4":
                            print("You chose:swapcase")
                            text = "Hello World"
                            print(text.swapcase())  # Output: "hELLO wORLD"

                    elif Case_Manipulation== "5":
                            print("You chose:return")

                            Case_Manipulation = False # when return before else 

                    else : 
                            print("Invalid input. Please choose between 1 and 5.")

            elif demo_choice == "3":
                print("You chose: Searching operations")
                String_loop = True 
                searching_sentance = input("Enter any sentance: ")
                searching_word =input("enter any word") 

                while String_loop:
                    print("1.find")
                    print("2.index ")
                    print("3.count ")
                    print("4.startswith")
                    print("5.endswith")
                    print("6.return")

                    choose = input("Select one from the above: ")
                    
                    if choose == "1":
                        print("You chose:find")
                        print(f"find result:{searching_sentance.find(searching_word )}")

                    elif choose == "2":
                        print("you chose :index ")  
                        print(f"index result:{searching_sentance.index(searching_word )}")


                    elif choose == "3":
                        print("You chose:count")
                        print(f"count result:{searching_sentance.count(searching_word )}")


                    elif choose == "4":
                        print("You chose:startswith")
                        print(f"startswith result:{searching_sentance.startwith(searching_word )}")
                            
                    elif choose == "5":
                        print("You chose:endswith")
                        print(f"endwith result:{searching_sentance.endwith(searching_word )}")
                            
                    elif choose == "6":
                        print("You chose:return")
                        String_loop = False # when return before else 

                    else : 
                        print("Invalid input. Please choose between 1 and 6.")


            elif demo_choice == "4":
                print("\nYou choose Slicing operations")
                slicing_sentance = input("Enter any sentance you wish to slice and eat :p  :")
                slicing_loop = True
                while slicing_loop:
                    print("/n1. Slice first 6 character")
                    print("2. Slice last 6 character")
                    print("3. Slice every other character")
                    print("4. Reverse your sentance")
                    print("5. Extract a specific word")
                    print("6. Return back to demonstration mode")
                    choose = input("Select from the above 1-5 and enjoy!  :  ")
                    # Slicing first 6 character
                    if choose == "1":
                        print("\nYou selected Slice first 6 character")
                        print(f"slicing firt 6 character result is = {slicing_sentance[:6]}")
                    #Slicing last 6 character
                    elif choose == "2":
                        print("\nYou selected Slice last 6 character")
                        print(f"slicing last 6 character result is = {slicing_sentance[-6:]}")
                    #Slice every other character
                    elif choose == "3":
                        print("\nYou selected Slice every other character")
                        print(f"Slice every other character result is = {slicing_sentance[::2]}")
                    #Reverse your sentance
                    elif choose == "4":
                        print("\nYou selected Reverse your sentance")
                        print(f"Reverse your sentance result is = {slicing_sentance[::-1]}")
                    #Extract a specific word
                    elif choose == "5":
                        print("\nYou selected Extract a specific word")
                        print(f"Extract a specific word result is = {slicing_sentance[3:10]}")
                    #Return back to demonstration menu
                    elif choose == "6":
                        print("\nReturning back to demonstration mode")
                        slicing_loop = False
                    else:
                        print("Invalid input. Please choose 1, 2, or 3.")

            elif demo_choice == "5":
                print("You chose: Split and join operations")
                # Split and join operations
                operation_loop=True 
                while operation_loop:

                    print ("enter a sentence")
                    print("1.String splitting")
                    print("2.joining ")
                    print("3.partition operations")
                    print("4.return")
                
                    choose =input("choose from 1-4")
                    sentence=input("enter any sentence")
                    
                    
                    if choose =="1":
                            print(sentence.split())
                        

                    elif choose =="2":
                            print ( " ".join(sentence))
                            
                    elif choose =="3":
                            print(sentence("@"))

                    elif choose=="4":
                            print("return")
                            operation_loop =False
                    else:
                            print("Invalid number, please choose from 1-4 !!! ")


            elif demo_choice == "6":
                print("You chose: Whitespace handling")
                print("You choose: Whitespace handling")
                whitespace_sentance = input("\nEnter any sentance with spaces form right, left, and in between :  ")
                print(f"\nStrip result = {whitespace_sentance.strip()}")
                print(f"Right Strip result = {whitespace_sentance.rstrip()}")
                print(f"Left Strip result = {whitespace_sentance.lstrip()}")

            elif demo_choice == "7":
                print("You chose: Character replacement")

                print("You choose: Character replacement")
                character_sentance = input("Enter a sentance: ")
                #Replace
                old = input("Enter a word or letter to replace: ")
                new = input(f"Enter what to replace '{old}' with: ")
                replaced_sentance = character_sentance.replace(old, new)
                print(f"\nReplace result = {replaced_sentance}")
                #Translate

                print("\nNow let's try replacing multiple characters at once (a > x, b > y, c > z)")
                trans_table = str.maketrans("abc", "xyz")
                translated_sentance = character_sentance.translate(trans_table)
                print(f"Translate result = {translated_sentance}")
        
            elif demo_choice == "8":
                print("You chose: String alignment")
                print("You choose: String alignment")
                string_alingment = input("Enter any word:   ")
                print(f"\nWidth = {string_alingment.center(20)}")
                print(f"Right just = {string_alingment.rjust(20)}")
                print(f"Left just = {string_alingment.ljust(20)}")


            elif demo_choice == "9":
                print("You chose: String validation")
                
                print("You choose: String validation")
                string_valid = input("Enter a string to validate: ")
                print(f"Is alphabetic (only letters)? {string_valid.isalpha()}")
                print(f"Is numeric (only digits)? {string_valid.isdigit()}")
                print(f"Is alphanumeric (letters or numbers)? {string_valid.isalnum()}")
                print(f"Is whitespace (only spaces)? {string_valid.isspace()}")
                print(f"Is uppercase? {string_valid.isupper()}")
                print(f"Is lowercase? {string_valid.islower()}")
                print(f"Is title case? {string_valid.istitle()}")
        
            elif demo_choice == "10":
                print("You chose: Formatting techniques")
                

                print("You choose: Formatting techniques")
                name = input("Enter your name: ")
                age = input("Enter your age: ")
                number = 10
                print(f"\nusing f-string: {name} is {age} years old!")
                print("using format(): {}".format("Hello,world!"))
                print("Using %% operator: %d%% of your name." % number)

            elif demo_choice == "11":
                print("Returning to main menu...")
                
                print("\nReturing to main menu .. :) ")
                Demonstration_running = False #Note: the loop here stops !and it returns to the main menu
     
                demo_running = False
            else:
                    print("Invalid value, please choose between 1 and 11")