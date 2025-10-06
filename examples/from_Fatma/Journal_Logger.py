
import datetime
import os
import shutil

#Creates new dated entry file.
def create_entry():
    from datetime import date
    today = str(date.today()) + ".txt"
    
    entry = input("Write your journal entry:\n")
    
    try:
        file = open(today, "w")
        file.write(entry + "\n")
        file.close()
        print("Entry saved!")
    except:
        print("Something went wrong while saving your entry.")


#Reads entries by date.
def read_entry():
    date_str = input("Enter the date of the entry to read (YYYY-MM-DD): ")
    filename = f"{date_str}.txt"

    try:
        with open(filename, "r") as file:
            print("\nEntry Content:")
            print(file.read())
    except FileNotFoundError:
        print("Entry not found for that date.")
    except Exception as e:
        print("Error reading entry:", e)

#Searches entries for keywords
def search_entries():
    keyword = input("Enter a word to search for: ").lower()
    found = False

    for file in os.listdir():
        if file.endswith(".txt"):
            try:
                with open(file, "r") as f:
                    content = f.read()
                    if keyword in content.lower():
                        print(f"Found in file: {file}")
                        found = True
            except:
                continue

    if not found:
        print("No entries found with that word.")

#Backs up entries periodically
def backup_entries():
    if not os.path.exists("journal_backup"):
        os.mkdir("journal_backup")

    for file in os.listdir():
        if file.endswith(".txt"):
            try:
                shutil.copy(file, "journal_backup")
            except:
                print("Could not back up:", file)

    print("Backup done.")

def menu():
    while True:
        print("\n Journal Menu:")
        print("1. Create a new entry")
        print("2. Read an entry by date")
        print("3. Search entries for keyword")
        print("4. Back up all entries")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")
        if choice == "1":
            create_entry()
        elif choice == "2":
            read_entry()
        elif choice == "3":
            search_entries()
        elif choice == "4":
            backup_entries()
        elif choice == "5":
            print("Thank you!")
            break
        else:
            print("Invalid choice. Try again.")

# Run the program
menu()
