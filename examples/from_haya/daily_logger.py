import sys         # to read system (command-line) arguments
import datetime    # to get today's date
import shutil      # to copy files (for backup)


# Create folders for journal entries and backups
JOURNAL_FOLDER = "examples/from_haya/entries"
BACKUP_FOLDER = "examples/from_haya/backup"

# Function to write a new journal entry
def write_entry():
    today = datetime.date.today().isoformat()  # format: YYYY-MM-DD
    file_path = f"{JOURNAL_FOLDER}/entries.txt"
    print(f"Write your journal entry for today: {today}")
    if len(sys.argv) != 3:
        print("invalid number of argument")
        return
    entry = today + ":" + sys.argv[2]
    with open(file_path, "a") as file:
        file.write(entry + "\n")
    print("Entry saved!")


# Function to read an entry by date (date passed from command line)
def read_entry():
    if len(sys.argv) != 2:
        print("Please provide a date like this: 2025-05-27")
        return
    date = sys.argv[1]
    file_path = f"{JOURNAL_FOLDER}/entries.txt"
    try:
        with open(file_path, "r") as file:
            print("\nJournal Entry:")
            print(file.read())
    except FileNotFoundError:
        print("No entry found for that date.")


# Function to search for a keyword (keyword passed from command line)
def search_entries():
    if len(sys.argv) != 3:
        print("Please provide a keyword to search for.")
        return
    keyword = sys.argv[2]
    found = False
    file_path = f"{JOURNAL_FOLDER}/entries.txt"
    with open(file_path, "r") as file:
        contents = file.readlines()
        for content in contents:
            if keyword in content:
                print(content)
    if not found:
        print("Keyword not found in any entry.")


# Function to backup all journal files
def backup_entries():
    if len(sys.argv) != 2:
        print("Please provide a keyword to search for.")
        return
    filepath = f"{JOURNAL_FOLDER}/entries.txt"
    backuppath = f"{BACKUP_FOLDER}/backup.txt"
    shutil.copy(filepath, backuppath)
    print("Backup completed successfully!")


# Menu for interactive use (optional)
def menu():
    choice = sys.argv[1]
    if choice == "write":
        write_entry()
    elif choice == "read":
        read_entry()
    elif choice == "search":
        search_entries()
    elif choice == "backup":
        backup_entries()
    else:
        print("Invalid option. Please try again.")

            
# Start the program
if __name__ == "__main__":
    menu()