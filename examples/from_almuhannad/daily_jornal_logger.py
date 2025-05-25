import os
import sys
from datetime import date



def create_entry(store,entry_txt):
    date = date.today().isformat()
    if date not in store:
        store[date] = []
    store[date].append(entry_txt)
    return store


def read_entry(read_date):
     with open(f"enteries/{read_date}.txt","r") as file:
        print(file.read())

def search_entry():
    found = False
    for filename in os.listdir("entries"):
        with open(f"entries/{filename}", "r") as file:
            content = file.read()
            print(f"Found in {filename}")
            found = True
    if not found:
        print("no entries matched your keyword")

command = sys.argv[1]

if command == "write":
    if len(sys.argv) < 3:
        print("Usage: python journal.py write 'your journal here")
    else:
        entry_txt = sys.argv[2]
        create_entry(entry_txt)

elif command == "read":
    if len(sys.argv) < 3:
        print("Usage: python journal.py read YYYY-MM-DD")
    else:
        read_entry(sys.argv[2])
    
elif command == "search":
    if len(sys.argv) < 3:
        print("Usage: python journal.py search keywords")
    else:
        print("unkown command. use write,read or search")
    
