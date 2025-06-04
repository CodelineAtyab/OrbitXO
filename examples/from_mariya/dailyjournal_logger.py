import os
import datetime
import shutil
import sys

JOURNAL_FOLDER = "examples/from_mariya/journal"
BACKUP_FOLDER = "examples/from_mariya/backup"

if not os.path.exists(JOURNAL_FOLDER):
    os.makedirs(JOURNAL_FOLDER)

if not os.path.exists(BACKUP_FOLDER):
    os.makedirs(BACKUP_FOLDER)

def write_entry():
    today = datetime.date.today().isoformat() #.isoformat() it converts a date into a string
    file_path = f"{JOURNAL_FOLDER}/data.txt"
    line = f"{today}:{sys.argv[2]}"
    try:
        with open(file_path, "a") as file:
            file.write(line + "\n")
        print("Entry saved.")
    except Exception as e:
        print("Error saving entry:", e)

def read_entry():
    file_path = f"{JOURNAL_FOLDER}/data.txt"

    try:
        with open(file_path, "r") as file:
            content = file.read()
        print(f"\nEntry for data.txt:\n{content}")
    except FileNotFoundError:
        print("No entry found for that date.")
    except Exception as e:
        print("Error reading entry:", e)

def search_entries():
    keyword = sys.argv[2].lower()
    found = False

    try:
        file_path = f"{JOURNAL_FOLDER}/data.txt"
        with open(file_path, "r") as file:
            contents = file.readlines()
            for content in contents:
                if keyword in content[content.index(":"):].lower():
                    found = True
                    print(content)
        if not found:
            print("No entries found with that keyword.")
    except Exception as e:
        print("Error during search:", e)

def backup_entries():
    try:
        src_path = f"{JOURNAL_FOLDER}/data.txt"
        dst_path = f"{BACKUP_FOLDER}/data.txt"
        shutil.copy(src_path, dst_path)
        print(f"All entries backed up to '{BACKUP_FOLDER}/'.")
    except Exception as e:
        print("Error during backup:", e)

def show_menu():
    choice = sys.argv[1]

    if choice == "write":
        write_entry()
    elif choice == "read":
        read_entry()
    elif choice == "search":
        search_entries()
    elif choice == "backup":
        backup_entries()
    elif choice == "exit":
        print("Goodbye.")
    else:
        print("Invalid choice.")

show_menu()