running = True
while running:
 print("\nMain menu :")
 print("1. Demonstration mode")
 print("2. Challenge mode")
 print("3. Exit")

 choose = input("select one from above (1, 2, or 3): ")
#Note: input means that the user should enter any number from 1-3  
 if choose == "1":
    print("\nYou selected Demonstration mode")
   
    # Demonstration mode submenu starts from here:
    Demonstration_running = True   
    
    #COMMENT:
    #IT'S manadatory to choose from 1-11, if not then the loop will return to
    #first step which is choose from (1-11)
    
    while Demonstration_running: #Note:while is under if conditon :) 
       print("\nDemonstration mode:")
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

       choose_Demonstration = input("\nSelect one from the above menu ( 1- 11 ): ")

       #Basic string properties coding starts here:
       if choose_Demonstration == "1":
          print("\n You choose basic string properties")
          
          basic_string_loop = True
          while basic_string_loop:
             print("\n1. Lenght")
             print("2. Concententation ")
             print("3. Repetition")
             print("4. Return back to demonstration menu ..")

             choose = input("Choose one from the above 1, 2, or 3 :")
             
             #Lenght coding starts from here:
             if choose == "1":
                print("\nYou selected Lenght, now let's count togather!")
                string_sentance = input("Enter your sentance here :")
                print(f"Lenght result : {len(string_sentance)} characters \nWell done!")

             #Concantentaion coding starts from here:
             elif choose == "2":
                print("\nYou selected concententaion, let's add your sentance to mine!")
                sentance = input("Enter your sentance: ")
                concententaion = sentance + ",I made it!"
                print(f"Concententation result : {concententaion} \nIt's nice, isn't hehehehe ?")
             
             #Repeition coding starts from here:
             elif choose == "3":
                print("\nYou selected repetition, let's repeat any word you want 3 times!")
                word = input("Enter any word to repeat:")
                repeated = word * 3
                print(f"Repetition result : {repeated} \nTolle arbeit!")

             #Retuning back to demonstration mode coding starts here:
             elif choose == "4":
                print("Returning back to demonstration mode")
                basic_string_loop = False

             else:
                print("Invalid number, please try again :( ")   
      
      #Case manipulation coding starts here:
       elif choose_Demonstration == "2":
          print("\nYou choose Case manipulation")
          case_mani_sentance = input("Enter any sentance : ")

          case_mani_loop = True
          while case_mani_loop:
             print("\n1. Uppercase")
             print("2. Lowercase")
             print("3. Title style")
             print("4. Swapcase")
             print("5. Return back to demonstration menu ..")

             choose = input("Choose one from above 1, 2, 3, or 4")
             #Uppercase
             if choose == "1":
                print("\nYou selected Uppercase:")
                print(f"Uppercase result : {case_mani_sentance.upper()}")
             #Lowercase
             elif choose == "2":
                print("\nYou selected Lowercase:")
                print(f"Lowercase result : {case_mani_sentance.lower()}")
             #Title style
             elif choose == "3":
                print("\nYou selected Title style:")
                print(f"Title style result : {case_mani_sentance.title()}")
             #Swapcase
             elif choose == "4":
                print("\nYou selected Swapcase:")
                print(f"Swapcase result : {case_mani_sentance.swapcase()}")
             #Return back to demanstration mode
             elif choose == "5":
                print("\nReturning back to demonstration mode")
                case_mani_loop = False

             else:
                print("Invalid number, please try again :( ")
                
      #Searching operation coding starts here:
       elif choose_Demonstration == "3":
          print("\nYou choose Searching operations")
         
          print("\nFirst let's add some sentances based on your preferance :)")
          searching_sentance = input("\nEnter any sentance : ")
          searching_word = input("Enter any word/letter to search : ")
          
          searching_loop = True
          while searching_loop:
             
             print("\n1. Find")
             print("2. Index")
             print("3. Count")
             print("4. Startswith")
             print("5. Endswith")
             print("6. Return back to demonstration mode")

             choose = input("Choose any searching operation you wish to discover from (1-5) :")
            
             #Find
             if choose == "1":
                print("\nYou selected Find operation")
                print(f"Find result : {searching_sentance.find(searching_word)}")
             #Index
             elif choose == "2":
                print("\nYou selected index operation")
                print(f"Index result : {searching_sentance.index(searching_word)}")
             #Count
             elif choose == "3":
                print("\nYou selected count operation")
                print(f"Count result : {searching_sentance.count(searching_word)}")
             #Startwith
             elif choose == "4":
                print("\nYou selected startwith operation")
                print(f"Index result : {searching_sentance.startswith(searching_word)}")
             #Endswith
             elif choose == "5":
                print("\nYou selected endswith operation")
                print(f"Index result : {searching_sentance.endswith(searching_word)}")
             #Return back to demanstration mode
             elif choose == "6":
                print("\nReturning back to demonstration mode")
                searching_loop = False
             else:
                print("Invalid number, please try again :( ")

       #Slicing operation coding starts here:
       elif choose_Demonstration == "4":
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
                print("Invalid number, please try again :( ")
                
       #Split and join coding starts form here:         
       elif choose_Demonstration == "5":
          print("You choose: Split, join, and partition operations")
          
          split_loop = True
          while split_loop:
             print("\n1. Split and join")
             print("2. Partition")
             print("3. Return back to demonstration mode")

             choose = input("Choose one from the above to try:  ")

             if choose == "1":
                print("\nYou selected Split and join")
                split_sentance = input("Enter your sentance, at least 3 words : ")
                #Split sentance
                split_words = split_sentance.split()
                #Join word
                join_with_hyphen = "-".join(split_words)

                print(f"\nSplit result = {split_words}")
                print(f"Join result = {join_with_hyphen}")

             elif choose == "2":
                print("You selceted Partition")
                partition = input("\nEnter any word that you would seperate around:  ")
                partition_result = split_sentance.partition(partition) #Partition() to break string into 3 parts
                print(f"\nPartition result = {partition_result}")
                
             elif choose == "3":
                print("Returning back to demonstration mode")
                split_loop = False

             else:
                print("Invalid number, try again!")
      
       #Whitespaces handling coding starts from here:
       elif choose_Demonstration == "6":
          print("You choose: Whitespace handling")

          whitespace_sentance = input("\nEnter any sentance with spaces form right, left, and in between :  ")
          print(f"\nStrip result = {whitespace_sentance.strip()}")
          print(f"Right Strip result = {whitespace_sentance.rstrip()}")
          print(f"Left Strip result = {whitespace_sentance.lstrip()}")

       #Replacement coding starts form here:
       elif choose_Demonstration == "7":
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

       #String alignment coding starts from here:
       elif choose_Demonstration == "8":
          print("You choose: String alignment")

          string_alingment = input("Enter any word:   ")

          print(f"\nWidth = {string_alingment.center(20)}")
          print(f"Right just = {string_alingment.rjust(20)}")
          print(f"Left just = {string_alingment.ljust(20)}")

       #String Alignment coding starts from here:
       elif choose_Demonstration == "9":
          print("You choose: String validation")
    
          string_valid = input("Enter a string to validate: ")

          print(f"Is alphabetic (only letters)? {string_valid.isalpha()}")
          print(f"Is numeric (only digits)? {string_valid.isdigit()}")
          print(f"Is alphanumeric (letters or numbers)? {string_valid.isalnum()}")
          print(f"Is whitespace (only spaces)? {string_valid.isspace()}")
          print(f"Is uppercase? {string_valid.isupper()}")
          print(f"Is lowercase? {string_valid.islower()}")
          print(f"Is title case? {string_valid.istitle()}")
   
       #Formatting techniques coding starts from here:
       elif choose_Demonstration == "10":
          print("You choose: Formatting techniques")

          name = input("Enter your name: ")
          age = input("Enter your age: ")

          # f string
          print(f"\nUsing f string: Hi my name is {name}, and I am {age} years old!")

          # .format()
          print("\nUsing .format():")
          print("Hello, {}! You are {} years old.".format(name, age))

          # % operator
          print("\nUsing % operator:")
          try:
           print("Hello, %s! You are %d years old." % (name, int(age)))
           print("Hint: %s for text, %d for numbers")
          except ValueError:
           print("Error: Age must be a number for %d formatting")

       elif choose_Demonstration == "11":
          print("\nReturing to main menu .. :) ")
          Demonstration_running = False #Note: the loop here stops !and it returns to the main menu
       else:
          print("Invalid value, please choose between 1 and 11")

 elif choose == "2":
    print("\nYou selected Challenge mode")

    # Challenge mode submenu starts from here:
    Challenge_running = True

    while Challenge_running:
     print("\nChallenge mode:")
     print("1. Challenge 1: Count the words with more than 3 letters ")
     print("2. Challenge 2: Convert 'hello world' to 'Hello-World'")
     print("3. Return to main menu")

     choose_challenge = input("Select one form the above 1,2, or 3 :")

     if choose_challenge == "1":
        print("\nYou selected challenge 1.")
        print("Given sentance: Mariya joined codeline as an AI operation")
        print("\ncount how many words have more than 3 letters ?")
        print("Type your answer, or type 'hint' to get some help :) ")

        #correct_answer = 4 >> this is not nessacery to be added !

        answering = True

        while answering:
           user_answer = input("\nYour answer is: ")
           if user_answer == "4":
              print("\nWell done! correct answer.")
              answering = False #If the answer = 4, the loop ends.
           elif user_answer.lower() == "hint": #.lower() used to ignors the capital letters
              print("\nHint: please break the sentance into words and count how many words > 3 letters ?")
           else:
              print("Invalid number, please type hint or try again !")

     elif choose_challenge == "2":
        print("\nYou selected challenge 2.")
        print("Question: Convert 'hello world' to 'Hello-World' ")
        print("Type your answer, or type 'hint' to get some help :) ")

        #correct_answer_1 = "Hello-World" >> This is not neccacsry to be added !

        Result = True

        while Result:
           user_answer = input("\nYour answer is: ")
           if user_answer == "Hello-World":
              print("Great job!")
              Result = False
           elif user_answer.lower() == "hint":
              print("\nHint: please capitalize first letter for each word and add - between them.")
           else:
              print("Incorrect answer, please type hint or try again ")

     elif choose_challenge == "3":
        print("Returing to main menu ..")
        Challenge_running = False
     else:
        print("Invalid value, please choose between 1 and 3")

 elif choose == "3":
    print("\nYou're exiting .. bye bye :)\n")
    running = False 
    """
    COMMENT:
    once number 3 is chosen to exit, then the loop stops, 
    as mentioned running = false
    """
 else:
    print("\nInvalid number, try again and please choose 1,2, or 3")