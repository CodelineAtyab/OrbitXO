import os
import sys
import datetime 

filepath = r".\examples\from_almuhannad\data.txt"
backups_file = r".\examples\from_almuhannad\backup.txt"
data_dict = {}

if not os.path.exists(filepath):
    try:
        with open(filepath, "w") as f:
            f.write("2000-11-11 : this a temp date\n")
        print(f"Created new file: {filepath}")
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
     print("file not found")
    except PermissionError:
     print("permission denaied")
    except Exception as e:
     print(f"there was an error: {e}")    
    return data_dict
          

def create_entry(data_dict,entry_txt):
    try:
        date_now = datetime.date.today().isoformat()
        entry_txt = " ".join(sys.argv[2:])

        if date_now not in data_dict:
            data_dict[date_now] = []
        data_dict[date_now].append(entry_txt)
        with open(filepath,"a") as f:
            f.write(f"{date_now} : {entry_txt}\n")
        return data_dict
    except FileNotFoundError:
     print("file not found")
    except PermissionError:
     print("permission denaied")
    except Exception as e:
     print(f"there was an error: {e}")

def read_entry(date_now):
    return data_dict.get(date_now, [])

        

def search_entry(data_dict, keyword):
    try:
        results = []
        for date, entries in data_dict.items():
            for entry in entries:
                if keyword.lower() in entry.lower():
                    results.append((date, entry))
        return results
    except FileNotFoundError:
     print("file not found")
    except PermissionError:
     print("permission denaied")
    except Exception as e:
     print(f"there was an error: {e}")

def backup_file():
    try:
        with open(filepath,"r") as file:
            new_file = file.read()
        with open(backups_file,"w") as file:
            file.write(new_file)
        return file
    except FileNotFoundError:
     print("file not found")
    except PermissionError:
     print("permission denaied")
    except Exception as e:
     print(f"there was an error: {e}")



data_dict = load_entries_from_file(filepath)
command = sys.argv[1]


if command == "write":
        entry_txt = sys.argv[2]
        data_dict = create_entry(data_dict,entry_txt)
        print(data_dict)

elif command == "read":
    entry_txt = sys.argv[2]
    entries = read_entry(entry_txt)
    if entries:
        print(f"Entries for {entry_txt}:")
        for entry in entries:
            print(f"- {entry}")
    else:
        print(f"No entries found for date: {entry_txt}")

    
elif command == "search":
    keyword = " ".join(sys.argv[2:])
    if keyword:
        results = search_entry(data_dict, keyword)
        if results:
            print(f"Search results for '{keyword}':")
            for date, entry_txt in results:
                print(f"{date}: {entry_txt}")
        else:
            print(f"No entries found for keyword: {keyword}")
    else:
        print("Please enter a keyword to search.")
elif command == "backup":
    backup_file()
else:
   print("no argument found")

    
