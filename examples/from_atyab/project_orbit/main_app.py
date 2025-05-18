import sys

import contact_book_utils


def say_end_of_script():
  print("End of Script")


if __name__ == "__main__":
  contacts_dict = {}

  contact_book_utils.load_contacts("./contacts.txt", contacts_dict)

  if sys.argv[1] in ["add", "update"]:
    contact_book_utils.add_contact(contacts_dict, sys.argv[2], sys.argv[3])
  elif sys.argv[1] == "view":
    contact_book_utils.view_contacts(contacts_dict)
  elif sys.argv[1] == "clear":
    contact_book_utils.clear_contacts(contacts_dict)
  
  say_end_of_script()