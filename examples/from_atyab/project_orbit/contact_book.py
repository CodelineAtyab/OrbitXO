import sys

contacts_dict = {}

if sys.argv[1] in ["add", "update"]:
  contacts_dict[sys.argv[2]] = sys.argv[3]
elif sys.argv[1] == "view":
  for key, value in contacts_dict.items():
    print(f"Contact No: {key}  --  Name: {value}")
elif sys.argv[1] == "clear":
  contacts_dict = {}

print(contacts_dict)