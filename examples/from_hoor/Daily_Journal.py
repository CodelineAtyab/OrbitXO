import os
import datetime
import shutil

# Create folders if they don't exist
journal_folder = "journal_entries"
backup_folder = "journal_backup"
os.makedirs(journal_folder, exist_ok=True)
os.makedirs(backup_folder, exist_ok=True)

def create_entry():
    today = datetime.date.today().isoformat()
    file_path = os.path.join(journal_folder, f"{today}.txt")
    
    if os.path.exists(file_path):
        print("Today's entry already exists.")
        return
    
    print("Write your entry (end with an empty line):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print("Entry saved.")
    except Exception as e:
        print("Something went wrong while saving the entry:", e)

def read_entry():
    date = input("Enter date (YYYY-MM-DD): ")
    file_path = os.path.join(journal_folder, f"{date}.txt")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            print("\n--- Entry ---")
            print(f.read())
    except FileNotFoundError:
        print("No entry found for that date.")
    except Exception as e:
        print("Error reading the file:", e)

def search_entries():
    keyword = input("Enter keyword to search: ").lower()
    found = False

    for filename in os.listdir(journal_folder):
        file_path = os.path.join(journal_folder, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if keyword in content.lower():
                    print(f"\n--- {filename} ---")
                    print(content)
                    found = True
        except Exception as e:
            print(f"Could not read {filename}:", e)
    
    if not found:
        print("No entries found with that keyword.")

def backup_entries():
    try:
        for filename in os.listdir(journal_folder):
            src = os.path.join(journal_folder, filename)
            dest = os.path.join(backup_folder, filename)
            shutil.copy2(src, dest)
        print("Backup completed.")
    except Exception as e:
        print("Error during backup:", e)

def menu():
    while True:
        print("\nMenu:")
        print("1. Write new entry")
        print("2. Read entry")
        print("3. Search entries")
        print("4. Backup entries")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_entry()
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
            print("Invalid option.")

if __name__ == "__main__":
    menu()
