import os              # Importing os to handle file operations
import datetime  # Importing datetime to handle dates
import shutil  # Importing shutil for file operations



def write_note():
    today = datetime.date.today().isoformat()
    file_name = f"journal_entries/{today}.txt"

    print(f"\nWrite your note for today {today} (type 'exit' to quit):")
    note = ""
    while True:
        line = input()
        if line.lower() == "exit":
            break
        note += line + "\n"

    with open(file_name, "a", encoding="utf-8") as file:
        file.write(note)
    print("Note saved.")

def read_note():
    date = input("Enter the date (e.g., 2025-05-28): ")
    file_name = f"journal_entries/{date}.txt"
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read()
            print("\nNote:\n")
            print(content)
    else:
        print("No note found for this date.")

def search_word():
    word = input("Enter the word you want to search for: ").lower()
    files = os.listdir("journal_entries")
    found = False

    for file_name in files:
        full_path = f"journal_entries/{file_name}"
        with open(full_path, "r", encoding="utf-8") as file:
            content = file.read()
            if word in content.lower():
                print(f"\nFound in: {file_name}")
                print(content)
                found = True

    if not found:
        print("The word was not found in any note.")

def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Write today's note")
        print("2. Read note by date")
        print("3. Search for a word")
        print("4. Exit")

        choice = input("Choose a number from 1 to 4: ")

        if choice == "1":
            write_note()
        elif choice == "2":
            read_note()
        elif choice == "3":
            search_word()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    menu()