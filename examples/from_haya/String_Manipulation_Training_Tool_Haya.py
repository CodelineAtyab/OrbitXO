def demonstration_mode():
    write_string = input("\nEnter a sample string: ")

    while True:
        print("\nSelect operation:")
        print("1. Basic string properties")
        print("2. Case manipulation ")
        print("3. Searching operations (find position)")
        print("4. Slicing operations")
        print("5. Split operation")
        print("6. Whitespace handling")
        print("7. Character replacement")
        print("8. String alignment")
        print("9. String validation")
        print("10. Formatting techniques")
        print("11. Return to main menu")

        oo = input("Choose an operation: ")

        if oo == "1":
            print("Length:", len(write_string))
            print("Concatenation:", write_string + " And fun too!")
            print("Repetition:", write_string * 2)

        elif oo == "2":
            print("Uppercase:", write_string.upper())
            print("Lowercase:", write_string.lower())
            print("Title case:", write_string.title())
            print("Swap case:", write_string.swapcase())

        elif oo == "3":
            word = input("Enter word to search for: ")
            print("Find position:", write_string.find(word))
            print("Count:", write_string.count(word))
            print("Starts with 'Haya'?", write_string.startswith("Haya"))
            print("Ends with 'learn'?", write_string.endswith("learn"))

        elif oo == "4":
            print("Every 2nd character:", write_string[::2])
            print("Last 5 characters:", write_string[-5:])
            print("Reversed:", write_string[::-1])

        elif oo == "5":
            print("Split:", write_string.split())
            joined = " ".join(write_string.split())
            print("Join with space:", joined)
            print("Partition 'powerful':", write_string.partition("powerful"))


        elif oo == "6":
            extra_space = "  " + write_string + "   "
            print("Original with spaces:", extra_space)
            print("Strip both sides:", extra_space.strip())
            print("Left strip:", extra_space.lstrip())
            print("Right strip:", extra_space.rstrip())
      

        elif oo == "7":
            print("Replace 'haya' with 'name':", write_string.replace("haya", "name"))

        elif oo == "8":
            print("Center text (50 chars):", write_string.center(50, "-"))
            print("Left-justify (50 chars):", write_string.ljust(50, "*"))
            print("Right-justify (50 chars):", write_string.rjust(50, "*"))

        elif oo == "9":
            print("Is all alphabetic?", write_string.isalpha())
            print("Is all digits?", write_string.isdigit())
            print("Is alphanumeric?", write_string.isalnum())
            print("Is all lowercase?", write_string.islower())
            print("Is all uppercase?", write_string.isupper())

        elif oo == "10":
            print(f"Using f-string: {write_string} has {len(write_string)} letters.")
            print("Using format(): {}".format("Hello world!"))
         

        elif oo == "11":
            break

        else:
            print("Invalid choice. Please try again.")
def main_menue()
# Main Program Execution
    while True:
        print("\nMain Menu:")
        print("1. Demonstration Mode")
        print("2. Exit")

        select = int(input("choose an option:"))

        if select == 1:
          demonstration_mode()
        elif select == 2:
          print("Goodbye!")
        break
    else:
         print("Invalid choice, try again.")