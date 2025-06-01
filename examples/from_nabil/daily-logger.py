import os
import sys
import datetime 

original_file = "./Nabil_file.txt"
backup_file = "./nabil_backup.txt"

data_dir = {}


if not os.path.exists(original_file):
    try:
        with open(original_file, "w") as f:
            f.write("This is a sample entry\n")
        print(f"new file created: {original_file}")

    except Exception as ex:
        print(f"file not created try again: {ex}")


def load_entries_from_file(path):
    try:
       with open(path, 'r') as f:
         for line in f:
           if ':' in line:
             date_str, entry_txt = line.strip().split(' : ', 1)
             date_new = datetime.datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()

             if date_new not in data_dir:
              data_dir[date_new] = []
              data_dir[date_new].append(entry_txt)

    except ValueError:
        print("Error date in file.")

    except FileNotFoundError:
        print("Error: File not found.")

    except PermissionError:
        print("Permission error.")

    except Exception as e:
        print(f"Error found: {e}")

    return data_dir


def create_entry(data_dir, entry_txt):
    try:
        date_now = datetime.date.today().isoformat()
        entry_txt = " ".join(sys.argv[2:])

        if date_now not in data_dir:
            data_dir[date_now] = []
        data_dir[date_now].append(entry_txt)

        with open(original_file, "a") as f:
            f.write(f"{date_now} : {entry_txt}\n")

        return data_dir
    
    except FileNotFoundError:
        print("File not found.")

    except PermissionError:
        print("Permission error.")

    except Exception as e:
        print(f"error found: {e}")


def read_entry(date_now):
    try: 
        return data_dir.get(date_now, [])
    
    except Exception as e:
        print(f"error found: {e}")

def search_entry(data_dir, keyword):
    try:
        results = []

        for date, entries in data_dir.items():
         for entry in entries:
             
             if keyword.lower() in entry.lower():
                 results.append((date, entry))

        return results
    
    except Exception as e:
        print(f"error found: {e}")

def backup_file():
    try:
        with open(original_file, "r") as file:
            content = file.read()

        with open(backup_file, "w") as file:
            file.write(content)

        print("Backup is created successfully.")

    except FileNotFoundError:
        print("File not found.")

    except PermissionError:
        print("Permission error.")

    except Exception as e:
        print(f"error found: {e}")

data_dir = load_entries_from_file(original_file)

if len(sys.argv) < 2:
    print("No command.")
    sys.exit()

command = sys.argv[1]

if command == "write":
    if len(sys.argv) < 3:
        print("provide text to write.")

    else:
        entry_txt = sys.argv[2]
        data_dir = create_entry(data_dir, entry_txt)
        print("Note added.")

elif command == "read":
    if len(sys.argv) < 3:
        print("provide a date to read.")

    else:
        date_str = sys.argv[2]
        entries = read_entry(date_str)
        if entries:
            print(f"Entries for {date_str}:")
            for entry in entries:
              print(f"- {entry}")

        else:
            print(f"entry not found for date: {date_str}")

elif command == "search":
    if len(sys.argv) < 3:
        print("search.")

    else:
        keyword = " ".join(sys.argv[2:])
        results = search_entry(data_dir, keyword)

        if results:
            print(f"Search results for '{keyword}':")

            for date, entry in results:
                print(f"{date}: {entry}")

        else:
            print(f"entry not found for containing '{keyword}'.")

elif command == "backup":
    backup_file()

else:
    print("Invalid command.")