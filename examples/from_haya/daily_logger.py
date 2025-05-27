import os
import datetime  
import shutil    #copying files

JOURNAL_FOLDER = "entries"    #where the jornal will save 
BACKUP_FOLDER = "backup"      #save backup for the jornal

os.makedirs(JOURNAL_FOLDER, exist_ok=True)   
os.makedirs(BACKUP_FOLDER, exist_ok=True)

def write_entry():
    today = datetime.date.today().isoformat()  #isoformat change string date to YYY-MM-DD
    file_path = f"{JOURNAL_FOLDER}/{today}.txt"
    print(f"Write your journal entry for today: {today}")
    entry = input(">>> ")
    with open(file_path, "a", encoding="utf-8") as file:    #use encoding so it support english,arabic and symbols
        file.write(entry + "\n") 
    print("Entry saved")

def read_entry():
    date = input("Enter date (e.g. 2025-05-27): ")
    file_path = f"{JOURNAL_FOLDER}/{date}.txt"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            print("\nJournal Entry:")
            print(file.read())
    else:
        print("No entry found for that date.")

def search_entries():
    keyword = input("Enter a keyword to search for: ")
    found = False
    for filename in os.listdir(JOURNAL_FOLDER):
        with open(f"{JOURNAL_FOLDER}/{filename}", "r", encoding="utf-8") as file:
            content = file.read()
            if keyword in content:
                print(f"\nFound in file: {filename}")
                print(content)
                found = True
    if not found:
        print("Keyword not found in any entry.")

def backup_entries():
    for filename in os.listdir(JOURNAL_FOLDER):
        source = f"{JOURNAL_FOLDER}/{filename}"
        destination = f"{BACKUP_FOLDER}/{filename}"
        shutil.copy(source, destination)
    print("Backup completed successfully!")

def menu():
    while True:
        print("\n--- Journal Menu ---")
        print("1. Write a New Entry")
        print("2. Read an Entry by Date")
        print("3. Search Entries")
        print("4. Backup All Entries")
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
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

menu()






