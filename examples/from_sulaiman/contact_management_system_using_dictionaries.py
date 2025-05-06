import string

contact_management_functional = True

contacts_list = []

while contact_management_functional:

    print("1. Add Contact\n"
    "2. Search Contact\n"
    "3. Update Contact\n"
    "4. Delete Contact\n"
    "5. List All Contacts\n"
    "6. Manage Groups\n"
    "7. Import/Export Contacts\n"
    "8. Exit")

    option = input("Choose option: ")

    if option == "1":
        first_name = input("First name: ").lower().strip()
        for first_name_char in first_name:
            if first_name_char not in list(string.ascii_lowercase):
                first_name = input("Invalid first name, try again: ").lower().strip()
        last_name = input("Last name: ").lower().strip()
        for last_name_char in last_name:
            if last_name_char not in (list(string.ascii_lowercase + " ")):
                first_name = input("Invalid last name, try again: ").lower().strip()
        phone_num = input("Phone number: ").lower().strip()
        while (not phone_num.isdigit()):
            phone_num = input("Phone number should include only digits: ").strip()
        while len(phone_num) < 8:
            phone_num = input("Phone number should be at least 8 characters long: ").lower().strip()
        email = input("Email(gmail, outlook, and yahoo): ").lower().strip()
        while "@" not in email:
            email = input("Email should contain an @ symbol: ").lower().strip()
        while not email.endswith(("@gmail.com", "@hotmail.com", "@yahoo.com")):
            email = input("Invalid domain name, try again: ").lower().strip()
        address = input("Address: ").lower().strip()
        group = input("Group (work/family/friends/other): ").lower().strip()
        contacts_list.append(dict(first_name = first_name, last_name = last_name, 
                            phone_number = phone_num, email_address = email,
                            home_address = address, group = group))
        print("Contact added successfully!\n")
    elif contacts_list == []:
        print("you have no contacts\n")
    elif option == "2":
        print("Search by:"
              "1. Name\n"
              "2. Phone\n"
              "3. Email\n"
              "4. Group\n")
        search_by = input("Choose search type: ")
        while search_by not in ["1", "2", "3", "4"]:
            search_by = input("Choose numbers between 1 and 4")
        if search_by == "1":
            search_first_name = input("Enter the first name: ").lower().strip()
            search_last_name = input("Enter the last name: ").lower().strip()
            found_search = False
            for contact in contacts_list:
                if search_first_name == contact.get("first_name") and \
                search_last_name == contact.get("last_name"):
                    print("found contact:")
                    print(contact)
                    found_search = True
                    break
            if not found_search:
                print("name not found")
        elif search_by == "2":
            search_phone_num = input("Enter the phone number: ").strip()
            found_search = False
            for contact in contacts_list:
                if search_phone_num == contact.get("phone_number"):
                    print("found contact:")
                    print(contact)
                    found_search = True
                    break
            if not found_search:
                print("phone number not found")
        elif search_by == "3":
            search_email = input("Enter the email: ").lower().strip()
            found_search = False
            for contact in contacts_list:
                if search_email == contact.get("email_address"):
                    print("found contact:")
                    print(contact)
                    found_search = True
                    break
            if not found_search:
                print("email not found")
        elif search_by == "4":
            search_group = input("Enter the group name: ").lower().strip()
            found_search = False
            for contact in contacts_list:
                if search_group == contact.get("group"):
                    print("found contact:")
                    print(contact)
                    found_search = True
                    break
            if not found_search:
                print("group not found")
    elif option == "3":
        update_first_name = input("Enter contact first name to update: ").lower().strip()
        update_last_name = input("Enter contact last name to update: ").lower().strip()
        found_update = False
        for contact in contacts_list:
            if update_first_name == contact.get("first_name") and \
                update_last_name == contact.get("last_name"):
                print("Select field to update:"
                      "1. Phone\n"
                      "2. Email\n"
                      "3. Address\n"
                      "4. Group\n")
                update_field = input("Choose update field: ")
                while update_field not in ["1", "2", "3", "4"]:
                    update_field = input("Choose between 1 and 4: ")
                if update_field == "1":
                    print("Current phone number: " + contact.get("phone_number"))
                    updated_phone_number = input("Enter new phone number: ").lower().strip()
                    while (not updated_phone_number.isdigit()):
                        updated_phone_number = input("Phone number should include only digits: ").lower().strip()
                    while len(updated_phone_number) < 8:
                        updated_phone_number = input("Phone number should be at least 8 characters long: ").lower().strip()
                    contact.update({"phone_number": updated_phone_number})
                    print("Phone number updated")
                    print(contact)
                if update_field == "2":
                    print("Current email address: " + contact.get("email_address"))
                    updated_email = input("Enter new email address(only gmail and microsoft for now): ").lower().strip()
                    while "@" not in updated_email:
                        updated_email = input("Email should contain an @ symbol: ").lower().strip()
                    while not updated_email.endswith(("gmail.com", "hotmail.com", "yahoo.com")):
                        updated_email = input("Invalid domain name, try again: ").lower().strip()
                    contact.update({"email_address": updated_email})
                    print("Email address updated")
                    print(contact)
                if update_field == "3":
                    print("Current home address: " + contact.get("home_address"))
                    updated_address = input("Enter new home address: ").lower().strip()
                    contact.update({"home_address": updated_address})
                    print("Home address updated")
                    print(contact)
                if update_field == "4":
                    print("Current group: " + contact.get("group"))
                    updated_group = input("Enter new group: ").lower().strip()
                    contact.update({"group": updated_group})
                    print("Group updated")
                    print(contact)
                found_update = True
                break
            if not found_update:
                ("Name isn't in list of contacts")
    elif option == "4":
        print("Select field to remove from\n"
              "1. Name\n"
              "2. Phone number\n"
              "3. Email\n")
        found = False
        remove_function = input("Choose a field:")
        while remove_function not in ["1", "2", "3"]:
            remove_function = input("Choose number between 1 and 3:")
        if remove_function == "1":
            remove_first_name = input("Enter first name of contact to remove: ").lower().strip()
            remove_last_name = input("Enter last name of contact to remove: ").lower().strip()
            for contact in contacts_list:
                if remove_first_name == contact.get("first_name") and \
                remove_last_name == contact.get("last_name"):
                    contacts_list.remove(contact)
                    found = True
                    break
            if not found:
                print("Name not found")
        if remove_function == "2":
            remove_phone = input("Enter phone number of contact to remove: ").lower().strip()
            for contact in contacts_list:
                if remove_phone == contact.get("phone_number"):
                    contacts_list.remove(contact)
                    found = True
                    break
            if not found:
                print("Name not found")
        if remove_function == "3":
            remove_email = input("Enter email address of contact to remove: ")
            for contact in contacts_list:
                if remove_email == contact.get("email_address"):
                    contacts_list.remove(contact)
                    found = True
                    break
            if not found:
                print("Name not found")
    elif option == "5":
        if contacts_list == []:
            print("you have 0 contacts")
        for contact in contacts_list:
            print(contact)
    elif option == "6":
        # contact_groups = []
        # for contact in contacts_list:
        #     if contact.get("group") not in contact_groups:
        print("to be continued")
    elif option == "7":
        print("to be continued")
    elif option == "8":
        print("End of program")
        contact_management_functional = False
    else:
        print("Choose a number between 1 and 8")