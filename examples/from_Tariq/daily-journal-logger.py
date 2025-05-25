import sys
import datetime
import os

def load_entries_from_file(file_path):
    data_store_dict = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if ':' in line:
                    date_str, entry = line.strip().split(' : ', 1)
                    try:
                        entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                        if entry_date not in data_store_dict:
                            data_store_dict[entry_date] = []
                        data_store_dict[entry_date].append(entry)
                    except ValueError:
                        continue
    except FileNotFoundError:
        return {}
    return data_store_dict

def create_new_dated_entry(data_store_dict, entry):
    entry_date = datetime.date.today()
    if entry_date not in data_store_dict:
        data_store_dict[entry_date] = []
    data_store_dict[entry_date].append(entry)
    return data_store_dict

def read_entry_by_date(data_store_dict, entry_date):
    return data_store_dict.get(entry_date, [])

def search_entries_by_keyword(data_store_dict, keyword):
    results = []
    for date, entries in data_store_dict.items():
        for entry in entries:
            if keyword.lower() in entry.lower():
                results.append((date, entry))
    return results

def back_up_entries(data_store_dict, backup_file):
    with open(backup_file, 'w') as f:
        for date, entries in data_store_dict.items():
            f.write(f"{date}:\n")
            for entry in entries:
                f.write(f"  - {entry}\n")
    print(f"Backup completed to {backup_file}")

FILE_PATH = 'journal.txt'
data_store_dict = load_entries_from_file(FILE_PATH)

if not os.path.exists(FILE_PATH):
    try:
        with open(FILE_PATH, "w") as f:
            f.write("yyyy-mm-dd : this a dummy entry\n")
        print(f"Created new file: {FILE_PATH}")
    except Exception as ex:
        print(f"Error creating file: {ex}")
        


if len(sys.argv) >= 2 and sys.argv[1].lower() == "entry":
    entry_text = " ".join(sys.argv[2:])
    if entry_text:
        data_store_dict = create_new_dated_entry(data_store_dict, entry_text)
        with open(FILE_PATH, "a") as f:
            f.write(f"{datetime.date.today()} : {entry_text}\n")
        print("Entry added successfully!")
    else:
        print("No entry text provided!")
else:
    print("Usage: python daily-journal-logger.py entry <your journal entry>")

if len(sys.argv) >= 2 and sys.argv[1].lower() == "read":
    try:
        entry_date = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
        entries = read_entry_by_date(data_store_dict, entry_date)
        if entries:
            print(f"Entries for {entry_date}:")
            for entry in entries:
                print(f"  - {entry}")
        else:
            print(f"No entries found for {entry_date}.")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

if len(sys.argv) >= 2 and sys.argv[1].lower() == "search":
    keyword = " ".join(sys.argv[2:])
    if keyword:
        results = search_entries_by_keyword(data_store_dict, keyword)
        if results:
            print(f"Search results for '{keyword}':")
            for date, entry in results:
                print(f"{date}: {entry}")
        else:
            print(f"No entries found containing '{keyword}'.")
    else:
        print("No keyword provided for search.")

if len(sys.argv) >= 2 and sys.argv[1].lower() == "backup":
    backup_file = sys.argv[2] if len(sys.argv) > 2 else "journal_backup.txt"
    back_up_entries(data_store_dict, backup_file)
    



    
