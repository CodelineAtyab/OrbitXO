all_contacts = {}
while True:
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. List All Contacts")
    print("6. Manage Groups")
    print("7. Import/Export Contacts")
    print("8. Exit")
    choice = input("Choose an option: ")
    if choice == "1":
        print("Enter Contact details:")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        name = first_name + " " + last_name
        phone = input("Phone: ")
        email = input("Email: ")
        address = input("Address: ")
        groups = input("Work/Family/Friends/Other: ")
        if phone in all_contacts:
            print("Error: This phone number already exists!")
        else:
            all_contacts[phone] = {
                'name': name,
                'phone': phone,
                'email': email,
                'address': address,
                'groups': groups
            }
            print("Contact added successfully!")
    elif choice == "2":
        print("Search by:")
        print("1. Name")
        print("2. Phone")
        print("3. Email")
        print("4. Group")
        search_by = input("Choose a Search type: ")
        found = False
        if search_by == "1":
            input_name = input("Enter first name and last name: ")
            for phone, contact in all_contacts.items():
                if contact['name'] == input_name:
                    print(f"Contact found: {phone} : {contact}")
                    found = True
                    break
            if not found:
                print("Contact not found")
        elif search_by == "2":
            input_phone = input("Enter a phone number: ")
            if input_phone in all_contacts:
                print(f"Contact found: {input_phone} : {all_contacts[input_phone]}")
                found = True
            else:
                print("Contact not found")
        elif search_by == "3":
            input_email = input("Enter your Email: ")
            for phone, contact in all_contacts.items():
                if contact['email'] == input_email:
                    print(f"Contact found: {phone} : {contact}")
                    found = True
                    break
            if not found:
                print("Contact not found")
        elif search_by == "4":
            input_groups = input("Enter your Group: ")
            for phone, contact in all_contacts.items():
                if contact['groups'] == input_groups:
                    print(f"Contact found: {phone} : {contact}")
                    found = True
            if not found:
                print("Contact not found")
    elif choice == "3":
        update_name = input("Enter first name and last name of contact to update: ")
        target_phone = None
        for phone, contact in all_contacts.items():
            if contact['name'] == update_name:
                target_phone = phone
                break
        if target_phone is None:
            print("Contact not found.")
        else:
            print("1. Phone")
            print("2. Email")
            print("3. Address")
            print("4. Groups")
            field_choice = input("Select field to update: ")
            if field_choice == "1":
                new_phone = input("Enter the new phone number: ")
                if new_phone in all_contacts and new_phone != target_phone:
                    print("Error: This phone number is already assigned to another contact.")
                else:
                    contact_data = all_contacts[target_phone].copy()
                    contact_data['phone'] = new_phone
                    all_contacts[new_phone] = contact_data
                    del all_contacts[target_phone]
                    print("Phone number updated successfully!")
            elif field_choice == "2":
                new_email = input("Enter new email: ")
                all_contacts[target_phone]['email'] = new_email
                print("Email updated successfully!")
            elif field_choice == "3":
                new_address = input("Enter new address: ")
                all_contacts[target_phone]['address'] = new_address
                print("Address updated successfully!")
            elif field_choice == "4":
                new_groups = input("Enter new Group (Work/Family/Friends/Other): ")
                all_contacts[target_phone]['groups'] = new_groups
                print("Group updated successfully!")
    elif choice == "4":
        print("Remove Contact")
        input_name = input("Enter the first name and last name of the contact to delete: ")
        target_phone = None
        for phone, contact in all_contacts.items():
            if contact['name'] == input_name:
                target_phone = phone
                break
        if target_phone:
            del all_contacts[target_phone]
            print(f"Contact '{input_name}' has been removed successfully.")
        else:
            print("Contact not found.")
    elif choice == "5":
        print("List all the Contacts")
        if not all_contacts:
            print("No contacts found.")
        else:
            for phone, contact in all_contacts.items():
                print(f"Name: {contact['name']}")
                print(f"Phone: {contact['phone']}")
                print(f"Email: {contact['email']}")
                print(f"Address: {contact['address']}")
                print(f"Group: {contact['groups']}")
                print("-" * 30)
    elif choice == "6":
        print("Manage Groups feature will be implemented in future updates.")
    elif choice == "7":
        print("Import/Export feature will be implemented in future updates.")
    elif choice == "8":
        print("Thank you for using the Contact Book. Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")
        