import os          # to work with folders and files
import sys         # to read system (command-line) arguments
import datetime    # to get today's date
import shutil      # to copy files (for backup)


# Create folders for journal entries and backups
JOURNAL_FOLDER = os.path.join(os.getcwd(), "entries")
BACKUP_FOLDER = os.path.join(os.getcwd(), "backup")

# Make sure folders exist
os.makedirs(JOURNAL_FOLDER, exist_ok=True)
os.makedirs(BACKUP_FOLDER, exist_ok=True)

# Function to write a new journal entry
def write_entry():
    today = datetime.date.today().isoformat()  # format: YYYY-MM-DD
    file_path = os.path.join(JOURNAL_FOLDER, f"{today}.txt")
    print(f"Write your journal entry for today: {today}")
    entry = input(">>> ")
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(entry + "\n")
    print("Entry saved!")


# Function to read an entry by date (date passed from command line)
def read_entry():
    if len(sys.argv) < 2:
        print("Please provide a date like this: 2025-05-27")
        return
    date = sys.argv[1]
    file_path = os.path.join(JOURNAL_FOLDER, f"{date}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            print("\nJournal Entry:")
            print(file.read())
    else:
        print("No entry found for that date.")


# Function to search for a keyword (keyword passed from command line)
def search_entries():
    if len(sys.argv) < 2:
        print("Please provide a keyword to search for.")
        return
    keyword = sys.argv[1]
    found = False
    for filename in os.listdir(JOURNAL_FOLDER):
        file_path = os.path.join(JOURNAL_FOLDER, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if keyword in content:
                print(f"\nFound in file: {filename}")
                print(content)
                found = True
    if not found:
        print("Keyword not found in any entry.")


# Function to backup all journal files
def backup_entries():
    for filename in os.listdir(JOURNAL_FOLDER):
        source = os.path.join(JOURNAL_FOLDER, filename)
        destination = os.path.join(BACKUP_FOLDER, filename)
        shutil.copy(source, destination)
    print("Backup completed successfully!")


# Menu for interactive use (optional)
def menu():
    while True:
        print("\n--- Journal Menu ---")
        print("1. Write a New Entry")
        print("2. Read an Entry (use: python daily_logger.py 2025-05-27)")
        print("3. Search Entries (use: python daily_logger.py keyword)")
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
            print("Invalid option. Please try again.")

            
# Start the program
if __name__ == "__main__":
    if len(sys.argv) == 1:
        menu()