import os
import sys
from datetime import date

filepath = r".\data.txt"

if not os.path.exists(filepath):
    try:
        with open(filepath, "w") as f:
            f.write("yyyy-mm-dd : this a data\n")
        print(f"Created new file: {filepath}")
    except Exception as ex:
        print(f"Error creating file: {ex}")
          

def create_entry(data_dict,entry_txt):
    date_now = date.today().isoformat()
    entry_txt = " ".join(sys.argv[2:])

    if date_now not in data_dict:
        data_dict[date_now] = []
    data_dict[date_now].append(entry_txt)
    with open(filepath,"a") as f:
        f.write(f"{date_now}:{entry_txt}")
    return data_dict


def read_entry(filepath):
    with open(filepath, "r") as file:
        content = file.read()
        print(content)
        

def search_entry(data_dict, keyword):
    results = []
    for date, entries in data_dict.items():
        for entry in entries:
            if keyword.lower() in entry.lower():
                results.append((date, entry))
    return results


data_dict = {}
command = sys.argv[1]


if command == "write":
        entry_txt = sys.argv[2]
        data_dict = create_entry(data_dict,entry_txt)
        print(data_dict)

elif command == "read":
        read_entry(filepath)
    
elif command == "search":
    keyword = " ".join(sys.argv[2:])
    if keyword:
        results = search_entry(data_dict, keyword)
        if results:
            print(f"Search results for '{keyword}':")
            for date, entry in results:
                print(f"{date}: {entry}")
        else:
            print("No entries matched your keyword.")
    else:
        print("Please enter a keyword to search.")

    
