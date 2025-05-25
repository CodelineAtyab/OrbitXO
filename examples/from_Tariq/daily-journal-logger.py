import sys
import datetime
import os

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

def main():
    FILE_PATH = 'journal.txt'
    data_store_dict = {}
    
   
    if not os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "w") as f:
                f.write("dd/mm/yyyy : this a dummy entry\n")
            print(f"Created new file: {FILE_PATH}")
        except Exception as ex:
            print(f"Error creating file: {ex}")
            return

    
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

if __name__ == "__main__":
    main()

    
 