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
                print("You chose: Basic string properties")
            elif demo_choice == "2":
                print("You chose: Case manipulation")
            elif demo_choice == "3":
                print("You chose: Searching operations")
            elif demo_choice == "4":
                print("You chose: Slicing operations")
            elif demo_choice == "5":
                print("You chose: Split and join operations")
            elif demo_choice == "6":
                print("You chose: Whitespace handling")
            elif demo_choice == "7":
                print("You chose: Character replacement")
            elif demo_choice == "8":
                print("You chose: String alignment")
            elif demo_choice == "9":
                print("You chose: String validation")
            elif demo_choice == "10":
                print("You chose: Formatting techniques")
            elif demo_choice == "11":
                print("Returning to main menu...")
                demo_running = False
            else:
                print("Invalid input. Please choose between 1 and 11.")

    elif choose == "2":
        print("\nYou selected Challenge Mode.")
        challenge_running = True
        while challenge_running:
            print("\nChallenge Menu:")
            print("1. Count words with more than 3 letters")
            print("2. Convert 'hello world' to 'Hello-World'")
            print("3. Return to main menu")

            ch_choice = input("Select one (1, 2, or 3): ").strip()

            if ch_choice == "1":
                print("\nChallenge 1:")
                print("Sentence: Mariya joined codeline as an AI operation")
                print("How many words have more than 3 letters?")
                print("Type your answer or type 'hint'.")

                correct = 5  # Words: Hoor, joined, codeline, operation, (maybe "code" if counted wrongly before)

                while True:
                    answer = input("Your answer: ").strip()
                    if answer == str(correct):
                        print("Well done! Correct answer.")
                        break
                    elif answer.lower() == "hint":
                        print("Hint: Count words longer than 3 letters.")
                    else:
                        print("Try again or type 'hint'.")

            elif ch_choice == "2":
                print("\nChallenge 2:")
                print("Convert 'hello world' to 'Hello-World'")
                print("Type your answer or type 'hint'.")

                correct = "Hello-World"

                while True:
                    answer = input("Your answer: ").strip()
                    if answer == correct:
                        print("Great job!")
                        break
                    elif answer.lower() == "hint":
                        print("Hint: Capitalize the first letters and replace space with '-'.")
                    else:
                        print("Try again or type 'hint'.")

            elif ch_choice == "3":
                print("Returning to main menu...")
                challenge_running = False
            else:
                print("Invalid input. Choose between 1 and 3.")

    elif choose == "3":
        print("Exiting the program. Goodbye! :)")
        running = False

    else:
        print("Invalid input. Please choose 1, 2, or 3.")
