import os
import datetime
import shutil

JOURNAL_FOLDER = "journal"
BACKUP_FOLDER = "backup"

if not os.path.exists(JOURNAL_FOLDER):
    os.makedirs(JOURNAL_FOLDER)

if not os.path.exists(BACKUP_FOLDER):
    os.makedirs(BACKUP_FOLDER)

def write_entry():
    today = datetime.date.today().isoformat() #.isoformat() it converts a date into a string
    file_path = os.path.join(JOURNAL_FOLDER, f"{today}.txt")

    print("Write your journal entry. Press Enter twice to save.")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    try:
        with open(file_path, "a") as file:
            file.write("\n".join(lines) + "\n")
        print("Entry saved.")
    except Exception as e:
        print("Error saving entry:", e)

def read_entry():
    date_str = input("Enter the date to read (YYYY-MM-DD): ")
    file_path = os.path.join(JOURNAL_FOLDER, f"{date_str}.txt")

    try:
        with open(file_path, "r") as file:
            content = file.read()
        print(f"\nEntry for {date_str}:\n{content}")
    except FileNotFoundError:
        print("No entry found for that date.")
    except Exception as e:
        print("Error reading entry:", e)

def search_entries():
    keyword = input("Enter a keyword to search: ").lower()
    found = False

    try:
        for filename in os.listdir(JOURNAL_FOLDER):
            file_path = os.path.join(JOURNAL_FOLDER, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().lower()
                if keyword in content:
                    print(f"Found in {filename}")
                    found = True
        if not found:
            print("No entries found with that keyword.")
    except Exception as e:
        print("Error during search:", e)

def backup_entries():
    try:
        for filename in os.listdir(JOURNAL_FOLDER):
            src_path = os.path.join(JOURNAL_FOLDER, filename)
            dst_path = os.path.join(BACKUP_FOLDER, filename)
            shutil.copy(src_path, dst_path)
        print(f"All entries backed up to '{BACKUP_FOLDER}/'.")
    except Exception as e:
        print("Error during backup:", e)

def show_menu():
    while True:
        print("\nJournal Menu:")
        print("1. Write a new entry")
        print("2. Read an entry by date")
        print("3. Search entries by keyword")
        print("4. Backup all entries")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            write_entry()
        elif choice == "2":
            read_entry()
        elif choice == "3":
            search_entries()
        elif choice == "4":
            backup_entries()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

show_menu()