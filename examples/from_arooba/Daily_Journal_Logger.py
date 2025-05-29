import os
import sys
import datetime

main_file = "arooba_diary.txt"
backup_path = "arooba_backup.txt"

data_dict = {}


if not os.path.exists(main_file):
    try:
        with open(main_file, "w") as f:
            f.write("2000-09-24 : This is a sample entry\n")
        print(f"Created new file: {main_file}")
    except Exception as ex:
        print(f"Error creating file: {ex}")


def load_entries_from_file(filepath):
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if ':' in line:
                    date_str, entry_txt = line.strip().split(' : ', 1)
                    date_now = datetime.datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()
                    if date_now not in data_dict:
                        data_dict[date_now] = []
                    data_dict[date_now].append(entry_txt)
    except ValueError:
        print("Error parsing date in file.")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return data_dict


def create_entry(data_dict, entry_txt):
    try:
        date_now = datetime.date.today().isoformat()
        entry_txt = " ".join(sys.argv[2:])

        if date_now not in data_dict:
            data_dict[date_now] = []
        data_dict[date_now].append(entry_txt)

        with open(main_file, "a") as f:
            f.write(f"{date_now} : {entry_txt}\n")
        return data_dict
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_entry(date_now):
    try: 
     return data_dict.get(date_now, [])
    except Exception as e:
        print(f"An error occurred: {e}")

def search_entry(data_dict, keyword):
    try:
        results = []
        for date, entries in data_dict.items():
            for entry in entries:
                if keyword.lower() in entry.lower():
                    results.append((date, entry))
        return results
    except Exception as e:
        print(f"An error occurred: {e}")

def backup_file():
    try:
        with open(main_file, "r") as file:
            content = file.read()
        with open(backup_path, "w") as file:
            file.write(content)
        print("Backup created successfully.")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"An error occurred: {e}")

data_dict = load_entries_from_file(main_file)

if len(sys.argv) < 2:
    print("No command provided.")
    sys.exit()

command = sys.argv[1]

if command == "write":
    if len(sys.argv) < 3:
        print("Please provide text to write.")
    else:
        entry_txt = sys.argv[2]
        data_dict = create_entry(data_dict, entry_txt)
        print("Note added successfully.")

elif command == "read":
    if len(sys.argv) < 3:
        print("Please provide a date (YYYY-MM-DD).")
    else:
        date_str = sys.argv[2]
        entries = read_entry(date_str)
        if entries:
            print(f"Entries for {date_str}:")
            for entry in entries:
                print(f"- {entry}")
        else:
            print(f"No entries found for date: {date_str}")

elif command == "search":
    if len(sys.argv) < 3:
        print("Please provide a keyword to search.")
    else:
        keyword = " ".join(sys.argv[2:])
        results = search_entry(data_dict, keyword)
        if results:
            print(f"Search results for '{keyword}':")
            for date, entry in results:
                print(f"{date}: {entry}")
        else:
            print(f"No entries found containing '{keyword}'.")

elif command == "backup":
    backup_file()

else:
    print("Invalid command. Use: write, read, search, or backup.")