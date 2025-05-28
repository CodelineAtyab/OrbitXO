import os
import shutil
from datetime import datetime

ENTRIES_FOLDER = "journal_entries"
BACKUP_FOLDER = "backups"

def ensure_folders():
    os.makedirs(ENTRIES_FOLDER, exist_ok=True)
    os.makedirs(BACKUP_FOLDER, exist_ok=True)

def get_entry_filename(date_str):
    return os.path.join(ENTRIES_FOLDER, f"{date_str}.txt")

def write_entry():
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = get_entry_filename(date_str)
    try:
        with open(filename, "a", encoding="utf-8") as file:
            print(f"Writing journal for {date_str}. Type your entry below (type 'END' to finish):")
            while True:
                line = input()
                if line.strip().upper() == "END":
                    break
                file.write(line + "\n")
        print("Entry saved.")
    except Exception as e:
        print("Error writing entry:", e)

def read_entry():
    date_str = input("Enter date to read (YYYY-MM-DD): ").strip()
    filename = get_entry_filename(date_str)
    try:
        with open(filename, "r", encoding="utf-8") as file:
            print(f"\n--- Journal Entry for {date_str} ---")
            print(file.read())
    except FileNotFoundError:
        print("No entry found for that date.")
    except Exception as e:
        print("Error reading entry:", e)

def search_entries():
    keyword = input("Enter keyword to search: ").strip().lower()
    found = False
    try:
        for file_name in os.listdir(ENTRIES_FOLDER):
            if file_name.endswith(".txt"):
                filepath = os.path.join(ENTRIES_FOLDER, file_name)
                with open(filepath, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    matches = [line for line in lines if keyword in line.lower()]
                    if matches:
                        print(f"\n--- Matches in {file_name} ---")
                        for line in matches:
                            print(line.strip())
                        found = True
        if not found:
            print("No matches found.")
    except Exception as e:
        print("Error searching entries:", e)

def backup_entries():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}")
        shutil.make_archive(backup_name, 'zip', ENTRIES_FOLDER)
        print("Backup completed successfully.")
    except Exception as e:
        print("Error during backup:", e)

def show_menu():
    ensure_folders()
    while True:
        print("\nJournal Menu:")
        print("1. Write new entry")
        print("2. Read entry by date")
        print("3. Search entries")
        print("4. Backup all entries")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()
        
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
            print("Invalid option. Please enter a number from 1 to 5.")

show_menu()
