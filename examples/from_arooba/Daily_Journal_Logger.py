import os
import datetime
import shutil

JOURNAL_DIR = "journal_entries"
BACKUP_DIR = "journal_backups"

# Ensure directories exist
os.makedirs(JOURNAL_DIR, exist_ok=True) # JOURNAL_DIR is where your journal entries are saved.
os.makedirs(BACKUP_DIR, exist_ok=True) # BACKUP_DIR is where your journal backups are saved.

def get_today_filename():
    today = datetime.date.today() # Get today's date.
    return os.path.join(JOURNAL_DIR, f"{today}.txt") # Create a filename for today's entry.

def write_entry():
    filename = get_today_filename()
    print("Write your journal entry. Type 'END' on a new line to finish.")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    
    with open(filename, "a", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")
    print(f"Entry saved to {filename}.")

def read_entry_by_date():
    date_str = input("Enter the date (YYYY-MM-DD): ")
    filename = os.path.join(JOURNAL_DIR, f"{date_str}.txt") # Create a filename for the specified date.
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file: # Open the file in read mode.
            print(f"\n--- Journal Entry for {date_str} ---")
            print(file.read())
    else:
        print("No entry found for that date.")

def search_entries():
    keyword = input("Enter a keyword to search: ").lower()
    found = False
    for filename in os.listdir(JOURNAL_DIR): # Iterate over all files in the journal directory.
        filepath = os.path.join(JOURNAL_DIR, filename) # Get the full path to the file.
        with open(filepath, "r", encoding="utf-8") as file: # Open the file in read mode.
            contents = file.read()
            if keyword in contents.lower():
                print(f"\nKeyword found in: {filename}")
                print(contents)
                found = True
    if not found:
        print("No entries found with that keyword.")

def backup_entries():
    for filename in os.listdir(JOURNAL_DIR):
        src = os.path.join(JOURNAL_DIR, filename)
        dst = os.path.join(BACKUP_DIR, filename)
        shutil.copy2(src, dst)
    print("Backup complete.")

def main():
    while True:
        print("\n--- Journal Menu ---")
        print("1. Write Entry")
        print("2. Read Entry by Date")
        print("3. Search Entries")
        print("4. Backup Entries")
        print("5. Exit")
        choice = input("Choose an option (1-5): ")

        try:
            if choice == "1":
                write_entry()
            elif choice == "2":
                read_entry_by_date()
            elif choice == "3":
                search_entries()
            elif choice == "4":
                backup_entries()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
