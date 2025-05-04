running = True
while running:
 print("Main menu :")
 print("1. Demonstration mode")
 print("2. Challenge mode")
 print("3. Exit")
 choose = input("select one from above (1, 2, or 3): ")
 if choose == "1":
    print("\nYou selected Demonstration mode")
    # Demonstration mode submenu starts from here:
    Demonstration_running = True
    while Demonstration_running:
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
# 1- Basic string properties ************************
       if choose_Demonstration == "1":
          print(" You choose: Basic string properties")

          string_tools_running = True
          while string_tools_running:
                    print("\nString Property Menu:")
                    print("1- Length")
                    print("2- Concatenation")
                    print("3- Repetition")
                    print("4- Exit to Demonstration menu")

                    sub_choice = input("Choose number from 1-4: ")

                    if sub_choice == "1":
                        user_string = input("Enter a sentence: ")
                        print("Length:", len(user_string), "characters")

                    elif sub_choice == "2":
                        str = input("Enter part: ")
                        result = str
                        print("Concatenation Result: ", result)

                    elif sub_choice == "3":
                        word = input("Enter a word to repeat: ")
                        times = int(input("How many times?: "))
                        print("Repetition Result:", word * times)

                    elif sub_choice == "4":
                        string_tools_running = False
                        print("Returning to Demonstration menu...")

                    else:
                        print("Invalid input. Please choose from 1 to 4.")

                    
# 2- Case manipulation ***********************************       
       elif choose_Demonstration == "2":
          print("**You choose: Case manipulation**")

          case_running=True
          while case_running:
             print(".\nCase manipulation Menu:")
             print("1- Upper \n2- Lower \n3- Title \n4- swapcase \n5- Exit to Demonstration menu")
             
             case_choose= input("Choose number:")
             if case_choose == "1":
                case_choose=input("Enter your sentence:")
                print("Looook, all the word with capital letters!!! =): "+ case_choose.upper())
             
             elif case_choose == "2":
                case_choose= input("Enter your sentance: ")
                print("Looook, all the word with small letters!!! =): "+ case_choose.lower())

             elif case_choose == "3":
                case_choose= input("Enter your sentance: ")
                print("Looook!!! =): "+ case_choose.title())

             elif case_choose == "4":
                case_choose= input("Enter your sentance: ")
                print("Looook!!!!!!! =): "+ case_choose.swapcase())

             elif case_choose == "5":
                case_running=False
                print("Returning to Demonstration menu...")
             
             else:
                print("Invalid input. Please choose from 1 to 5.")
                
            
# 3- Searching operations ***********************************      
       elif choose_Demonstration == "3":
          print("You choose: Searching operations")

          ops_running= True
          while ops_running:
             print("Searching operations menu:")
             print("1- Find \n2- index \n3- count \n4- startswith \n5- endswith \n6- Exit")
             ops_running= input("Choose number from 1-6: ")

             if ops_running =="1":
               text= "\nPython is easy to learn"
               print(text)
               print("Find function in 'easy':", text.find("easy"))
               
             elif ops_running =="2":
               ops_running= "\nAI operation team is cool"
               print(ops_running)
               print("index functon in 'cool': ", ops_running.index("cool")) 

             elif ops_running == "3":
               ops_running="\npython is powerful and python is easy"
               print(ops_running)
               print("Count the word 'python': ", ops_running.count("python"))
           
             elif ops_running == "4":
               ops_running= "python is easy to learn"
               print(ops_running)
               print("The word 'python':  ", ops_running.startswith("python"))
               print("The word 'easy':  ", ops_running.startswith("easy"))

             elif ops_running =="5":
               ops_running= "\nAI and ML are popular"
               print(ops_running)
               print("The word 'popular':  ", ops_running.endswith("popular"))
               print("the word 'AI':  ", ops_running.endswith("AI"))
             
             elif ops_running =="6":
               ops_running= False
               print("Returning to Demonstration menu...")

             else:
               print("Invalid input. Please choose from 1 to 6.")
             
# 4- Slicing operations ********************************         
       elif choose_Demonstration == "4":
          print("You choose: Slicing operations")

          string_running= True
          while string_running:
             print("Slicing operations Menu:")
             print("1- Basic slicing \n2- Slicing without start \n3- Slicing without end \n4- Exit")
             string_running=input("Choos number from 1-4:\n")

             if string_running =="1":
                string_running= "PythonProgramming"
                print(string_running)
                print("print [0:6]:  ", string_running[0:6])

             elif string_running == "2":
                string_running= "PythonProgramming"
                print(string_running)
                print("print [6: ]:  ", string_running[:6])

             elif string_running == "3":
                string_running= "PythonProgramming"
                print(string_running)
                print("print [6: ]:  ", string_running[6:])

             elif string_running == "4":
                string_running= False
                print("Returning to Demonstration menu...")

             else:
               print("Invalid input. Please choose from 1 to 4.")

# 5- Split and join operations ***************************
       elif choose_Demonstration == "5":
          print("You choose: Split and join operations")

          split_running =True
          while split_running:
             print("Split and join operations menu:")
             print("1- split \n2- join \n3- partition \n 4- Exit")
             split_running= input("Choose number from 1-4:  ")

             if split_running == "1":
               split_running= "Python is easy to learn"
               print(split_running)
               print(split_running.split())

             elif split_running == "2":
               split_running= ['Python','is','easy','to','learn']
               print(split_running)
               print(" ".join(split_running))

             elif split_running == "3":
                split_running="Python is easy to learn"
                print(split_running)
                print(split_running.partition("is easy"))

             elif split_running == "4":
                split_running = False
                print("Returning to Demonstration menu...")

             else:
                print("Invalid input. Please choose from 1 to 4.")

# 6- Whitespace handling *********************************
  # 1. strip() — Remove both leading and trailing
       elif choose_Demonstration == "6":
          print("You choose: Whitespace handling")
          whitspace_running=True
          while whitspace_running:
             print("Whitespace handling Menu:")
             print("1- strip \n2- Istrip \n3- rstrip \n4- Exit")
             whitspace_running= input("Choose number:")

             if whitspace_running == "1":
               whitspace_running= "   Python is cool   "
               print(whitspace_running)
               print(whitspace_running.strip())

  # 2. lstrip() — Remove whitespace from the left side
             elif whitspace_running == "2":
               whitspace_running= "   Python is cool   "
               print(whitspace_running)
               print(whitspace_running.lstrip())

  # 3. rstrip() — Remove whitespace from the right side
             elif whitspace_running == "3":
               whitspace_running= "   Python is cool   "
               print(whitspace_running)
               print(whitspace_running.rstrip())
             
             elif whitspace_running == "4":
               whitspace_running = False
               print("Returning to Demonstration menu...")

             else:
               print("Invalid input. Please choose from 1 to 4.")
             

#7- Character replacement *********************
       elif choose_Demonstration == "7":
          print("You choose: Character replacement")

          rep_running= True
          while rep_running:
             print("Character replacement menu:")
             print("1- replacement \n2- translate \n3- Exit")
             rep_running= input("Choose number:")

             if rep_running == "1":
               rep_running="I like Python. Python is fun."
               print(rep_running)
               print("Replace the word 'Java' in 'Python': ", rep_running.replace("Python", "Java"))

             elif rep_running == "2":
                rep_running="hello world"
                print(rep_running)
                table = str.maketrans("aeiou", "12345")
                print(rep_running.translate(table))

             elif rep_running== "3":
                whitspace_running = False
                print("Returning to Demonstration menu...")

             else:
               print("Invalid input. Please choose from 1 to 3.")
                

# 8- String alignment *************************        
       elif choose_Demonstration == "8":
          print("You choose: String alignment")

          string_running= True
          while string_running:
             print("String alignment menu:")
             print("1-center \n2- ljust \n3- rjust \n4- Exit")
             string_running=input("Choose number: ")

             if string_running == "1":
                string_running="Python"
                print(string_running)
                print(string_running.center(20, "-"))

             elif string_running == "2":
                string_running= "Python"
                print(string_running)
                print(string_running.ljust(20, "*"))

             elif string_running == "3":
                string_running= "Python"
                print(string_running)
                print(string_running.rjust(20, "*"))
             
             elif string_running == "4":
                string_running= False
                print("Returning to Demonstration menu...")

             else:
               print("Invalid input. Please choose from 1 to 4.")

# 9- String validation *****************************
       elif choose_Demonstration == "9":
          print("You choose: String validation")

          val_running= True
          while val_running:
             print("1-isalpha \n2- isdigit \n3- Exit")
             val_running= input("Choose number: ")

  #1.isalpha()Returns True if all characters in the string are letters (A–Z or a–z), and the string is not empty.
             if val_running =="1":
                val_running="Hello"
                print(val_running)
                print(val_running.isalpha())  
                val_running1= "Hello123"
                print(val_running1)
                print(val_running1.isalpha())

  #2.isdigit()Returns True if all characters are digits (0–9), and the string is not empty.
             elif val_running== "2":
                val_running="112233"
                print(val_running)
                print(val_running.isdigit())  
                val_running1= "Hello123"
                print(val_running1)
                print(val_running1.isdigit())

             elif val_running== "3":
                val_running=False
                print("Returning to Demonstration menu...")

             else:
               print("Invalid input. Please choose from 1 to 3.")
                

# 10- Formatting techniques *************************
       elif choose_Demonstration == "10":
          print("You choose: Formatting techniques")

          for_running=True
          while for_running:
             print("Formatting techniques menu:")
             print("1- f-Strings \n2- format() \n3- Exit ")
             for_running=input("Choose number: ")

             if for_running =="1":
                name = "Arooba"
                age = 25
                print(f"My name is {name} and I am {age} years old.")

             elif for_running =="2":
                name = "Arooba"
                score = 92.5
                print("Student: {}, Score: {}".format(name, score))
                
             elif for_running=="3":
                for_running=False
                print("Returning to Demonstration menu...")

             else:
               print("Invalid input. Please choose from 1 to 3.")

            
       elif choose_Demonstration == "11":
          print("\nReturing to main menu .. :) ")
          Demonstration_running = False
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
        print("Given sentance: Arooba joined codeline as an AI operation")
        print("\ncount how many words have more than 3 letters ?")
        print("Write your answer, or type 'hint' to get some help :) ")
        
        answering = True
        while answering:
           user_answer = input("\nYour answer is: ")
           if user_answer == "4":
              print("\nWell done! correct answer.")
              answering = False
           elif user_answer.lower() == "hint":
              print("\nHint: please break the sentance into words and count how many words > 3 letters ?")
           else:
              print("Invalid number, please type hint or try again !")

     elif choose_challenge == "2":
        print("You selected challenge 2.")
        print("Convert 'hello world' to 'Hello-World' ")
        choose_challenge= input("Your answer is:")
        if choose_challenge == "Hello_World":
          print("Well done!!!! correct answer =)")
          
     elif choose_challenge == "3":
        Challenge_running = False
        print("Returing to main menu ..")
        
     else:
        print("Invalid value, please choose between 1 and 3")
 elif choose == "3":
    print("\nYou're exiting .. bye bye :)\n")
    running = False
 else:
    print("\nInvalid number, try again and please choose 1,2, or 3")