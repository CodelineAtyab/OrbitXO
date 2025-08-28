import os              # Importing os to handle file operations
import datetime  # Importing datetime to handle dates
import sys


def write_note():
    today = datetime.date.today().isoformat()
    file_name = f"journal_entries/{today}.txt"
    note = sys.argv[2] if len(sys.argv) > 2 else ""
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(note)
    print("Note saved.")

def read_note():
    date = sys.argv[2] if len(sys.argv) > 2 else datetime.date.today().isoformat()
    file_name = f"journal_entries/{date}.txt"
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read()
            print("\nNote:\n")
            print(content)
    else:
        print("No note found for this date.")

def search_word():
    word = sys.argv[2].lower()
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
 

    choice = sys.argv[1] if len(sys.argv) > 1 else None 

    if choice == "1":
        write_note()
    elif choice == "2":
        read_note()
    elif choice == "3":
        search_word()
    else:
        print("Invalid choice, try again.")

if __name__ == "__main__":
    menu()