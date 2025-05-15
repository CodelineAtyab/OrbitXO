import sys

contacts_dict = {}

# Point to the file
contacts_to_load_file = open("./contacts.txt", "r")

# Load the dictionary with saved entries
lines_of_data = contacts_to_load_file.readlines()
contacts_to_load_file.close()

for line in lines_of_data:
  line = line.strip().split(",")
  contact_no = line[0]
  contact_name = line[1]
  # print(contact_no, contact_name)
  contacts_dict[contact_no] = contact_name



if sys.argv[1] in ["add", "update"]:
  contacts_dict[sys.argv[2]] = sys.argv[3]
  contacts_file = open("./contacts.txt", "a")
  contacts_file.write(f"{sys.argv[2]},{sys.argv[3]}\n")
  contacts_file.close()
elif sys.argv[1] == "view":
  for key, value in contacts_dict.items():
    print(f"Contact No: {key}  --  Name: {value}")
elif sys.argv[1] == "clear":
  contacts_dict = {}

print("End of Script")