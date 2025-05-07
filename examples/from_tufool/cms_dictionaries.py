all_contacts = {}
menu= True
while menu:
    print("\nContact Book System")
    print("1. Add Contact")
    print("2. Search Contacts")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. Exit")
    choice = input("Choose an option: ")
    if choice == '1':
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        name = first_name + " " + last_name
        if name in all_contacts:
            print("Contact already exists.")
            continue
        phone = input("Phone: ")
        email = input("Email: ")
        address = input("Address: ")
        group = input("Group (work/family/friends/other): ")
        all_contacts[name] = {'phone': phone, 'email': email, 'address': address, 'group': group}
        print(f"Contact {name} added successfully.")
    elif choice == '2':
        print("Search by:\n 1. Name\n 2. Phone\n 3. Email\n 4. Group")
        search_choice = input("Choose search type: ")
        found = False
        if search_choice == '1':
            input_name = input("Enter contact name: ")
            if input_name in all_contacts:
                print(f"Found: {input_name}: {all_contacts[input_name]}")
                found = True
        elif search_choice == '2':
            input_phone = input("Enter phone number: ")
            for name, details in all_contacts.items():
                if details['phone'] == input_phone:
                    print(f"Found: {name}: {details}")
                    found = True
                    break
        elif search_choice == '3':
            input_email = input("Enter email: ")
            for name, details in all_contacts.items():
                if details['email'] == input_email:
                    print(f"Found: {name}: {details}")
                    found = True
                    break
        elif search_choice == '4':
            input_group = input("Enter group: ")
            for name, details in all_contacts.items():
                if details['group'] == input_group:
                    print(f"{name}: {details}")
                    found = True
        if not found:
            print("No contacts found.")
    elif choice == '3':
        name = input("Enter full name of the contact to update: ")
        if name in all_contacts:
            print("1. Phone\n2. Email\n3. Address\n4. Group")
            field_choice = input("Choose field to update: ")
            if field_choice == '1':
                new_value = input("Enter new phone: ")
                all_contacts[name]['phone'] = new_value
            elif field_choice == '2':
                new_value = input("Enter new email: ")
                all_contacts[name]['email'] = new_value
            elif field_choice == '3':
                new_value = input("Enter new address: ")
                all_contacts[name]['address'] = new_value
            elif field_choice == '4':
                new_value = input("Enter new group: ")
                all_contacts[name]['group'] = new_value
            else:
                print("Invalid field.")
                continue
            print("Contact updated successfully.")
        else:
            print("Contact not found.")
    elif choice == '4':
        name = input("Enter full name of the contact to delete: ")
        if name in all_contacts:
            del all_contacts[name]
            print("Contact deleted successfully.")
        else:
            print("Contact not found.")
    elif choice == '5':
        print("Goodbye!")
        menu = False  