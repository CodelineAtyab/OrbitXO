import utils

# The utility functions or procedures would be here
def add_contact(data_store_dict, phone_no, name):
  data_store_dict[phone_no] = name
  utils.write_dict_entry_to_file(phone_no, name)


def view_contacts(data_store_dict):
  for key, value in data_store_dict.items():
    print(f"Contact No: {key}  --  Name: {value}")


def clear_contacts(data_store_dict):
  data_store_dict = {}


def load_contacts(file_path, data_store_dict):
  # Point to the file
  contacts_to_load_file = open(file_path, "r")

  # Load the dictionary with saved entries
  lines_of_data = contacts_to_load_file.readlines()
  contacts_to_load_file.close()

  for line in lines_of_data:
    line = line.strip().split(",")
    contact_no = line[0]
    contact_name = line[1]
    # print(contact_no, contact_name)
    data_store_dict[contact_no] = contact_name

if __name__ == "__main__":
  print("Running some tests")
  clear_contacts({})
  print("Done Running some tests")
