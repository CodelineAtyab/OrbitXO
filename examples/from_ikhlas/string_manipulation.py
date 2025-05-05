
#using function to define the menu
def main_menu():
    while True:
        print("\nMAIN MENU")
        print("1.Demonstration Mode")
        print("2.Challenge Mode")
        print("3.Exit")
        option = input("Choose an option: ")

        if option == "1":
            demonstration_mode()
        elif option == "2":
            challenge_mode()
        elif option == "3":
            print("Goodbye!")
            exit
        else: #for the numbers other than 1 or 2 or 3
            print("Please enter 1, 2, or 3.")

def demonstration_mode():
    user_input = input("\nEnter a string to work with: ")

    while True:
        print("\nDEMONSTRATION MENU")
        print("1.Basic string properties")
        print("2.Case manipulation")
        print("3.Search operation")
        print("4.Slicing operation")
        print("5.Split and join operation")
        print("6.Whitespace handling")
        print("7.Character replacement")
        print("8.String alignment")
        print("9.String validation")
        print("10.Formatting techniques")
        print("11.Return to main menu")

        option = input("\nChoose an operation: ")

        if option == "1":
            print("\nBasic string properties")
            print("Length:",len(user_input))   #for the string length 
            print("Concatination: ",user_input+" is fun!")
            print("Repetition result: ",user_input * 3)

        elif option == "2":
            print("\nUppercase:", user_input.upper())
            print("Lowercase:", user_input.lower())
            print("Title Case:", user_input.title())
            print("Swap Case:", user_input.swapcase())

        elif option == "3":
            print("\nFind 'ph':", user_input.find("ph"))
            print("Count 'a':", user_input.count("a"))
            print("Starts with 'Hello':", user_input.startswith("Hello"))
            print("Ends with '!':", user_input.endswith("!"))

        elif option == "4":
            print("Slicing operation:")
            print("\nFirst 6 letters:", user_input[:6])
            print("Last 6 letters:", user_input[-6:])
            print("Every other charachters:", user_input[::2])
            print("Reverse string:", user_input[::-1])
            

        elif option == "5":
            words = user_input.split()
            print("\nSplit into words:", words)
            print("Join with '-':", "-".join(words)) 

        elif option == "6":
            text = "   " + user_input + "   "
            print("\nOriginal text with spaces: '" + text + "'")
            print("strip():", text.strip())
            print("lstrip():", text.lstrip())
            print("rstrip():", text.rstrip())

        elif option == "7":
            print("\nReplace 'a' with '@':", user_input.replace("a", "@"))

        elif option == "8":
            print("\nCenter text (40 chars):", user_input.center(40, "*"))
            print("Left aligned:", user_input.ljust(40, "-"))
            print("Right aligned:", user_input.rjust(40, "-"))

        elif option == "9":
            print("\nIs only letters?", user_input.isalpha())  #if all characters in user_input are alphabetic 
            print("Is only numbers?", user_input.isdigit())  #if all characters in user_input are digits
            print("Is letters and numbers?", user_input.isalnum())  #if all characters in user_input are either letters or digits, with at least one character.

        elif option == "10":
            name= "Ikhlas"
            print("Formatting techniques: \nUsing f-string:")
            print(f"Result: Ikhlas name has" ,{len(name)} , "letters.")
            print("%d%% of Python developers love string manipulation" % 90)

        elif option == "11":
            break
        else:
            print("Invalid option, try again.")

def challenge_mode():
    print("\nWelcome to Challenge Mode!")
    print("Try solving small problems with strings.")
    

    # Challenge 1
    ch_input = input("Enter challenge sentence: ")
    words = ch_input.split()
    count = 0
    for word in words:
        if len(word) > 3:
            count += 1
    print("Number of words with more than 3 letters:", count)
    
    
    #Challenge 2 
    print("\nChallenge 2:")
    answer = input("Enter challenge sentence: ")
    title = (answer.title())
    print(title.replace(" ", "-"))



if __name__ == "__main__":  #to control the execution of code 
    main_menu() #to run only the main menue 
