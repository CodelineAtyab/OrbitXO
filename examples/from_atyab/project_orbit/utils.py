def write_dict_entry_to_file(key, value):
  contacts_file = open("./contacts.txt", "a")
  contacts_file.write(f"{key},{value}\n")
  contacts_file.close()
