running = True
#COMMENT:
#once number 1 or 2 is chosen, then the loop starts the process, 
#as mentioned running = True

while running:
 print("Main menu :")
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
                print(f"Concententation result : {concententaion} \nIt's nice, isn't heheheh ?")
             
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
      
      
       elif choose_Demonstration == "2":
          print("You choose: Case manipulation")
       elif choose_Demonstration == "3":
          print("You choose: Searching operations")
       elif choose_Demonstration == "4":
          print("You choose: Slicing operations")
       elif choose_Demonstration == "5":
          print("You choose: Split and join operations")
       elif choose_Demonstration == "6":
          print("You choose: Whitespace handling")
       elif choose_Demonstration == "7":
          print("You choose: Character replacement")
       elif choose_Demonstration == "8":
          print("You choose: String alignment")
       elif choose_Demonstration == "9":
          print("You choose: String validation")
       elif choose_Demonstration == "10":
          print("You choose: Formatting techniques")
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