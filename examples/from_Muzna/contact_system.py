contacts={}

while True:
    print("\nContact Book System")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. List All Contacts")
    print("6. Exit")

    choice = input("Choose an option: ")
    if choice == "1":
        full_name = input("Enter full name: ")
        if full_name in contacts:
            print("Contact already exists.")
        else:
            phone = input("Phone: ")
            email = input("Email: ")
            address = input("Address: ")
            group = input("Group (work/family/friends/other): ")
            contacts[full_name] = {
                "phone": phone,
                "email": email,
                "address": address,
                "group": group
            }
            print("Contact added successfully!")
    elif choice == "2":
        print("Search by:\n1. Name\n2. Phone\n3. Email")
        search_type = input("Choose search type: ")

        if search_type == '1':
            name_input = input("Enter name: ").lower()
            found = False
            for full_name in contacts:
                if name_input in full_name.lower():
                    print("\nName:", full_name)
                    print("Phone:", contacts[full_name]['phone'])
                    print("Email:", contacts[full_name]['email'])
                    print("Address:", contacts[full_name]['address'])
                    print("Group:", contacts[full_name]['group'])
                    found = True
            if not found:
                print("Contact not found.")

        elif search_type == '2':
            phone_input = input("Enter phone number: ")
            found = False
            for full_name in contacts:
                if phone_input == contacts[full_name]['phone']:
                    print("\nName:", full_name)
                    print("Phone:", contacts[full_name]['phone'])
                    print("Email:", contacts[full_name]['email'])
                    print("Address:", contacts[full_name]['address'])
                    print("Group:", contacts[full_name]['group'])
                    found = True
            if not found:
                print("Contact not found.")

        elif search_type == '3':
            email_input = input("Enter email: ")
            found = False
            for full_name in contacts:
                if email_input == contacts[full_name]['email']:
                    print("\nName:", full_name)
                    print("Phone:", contacts[full_name]['phone'])
                    print("Email:", contacts[full_name]['email'])
                    print("Address:", contacts[full_name]['address'])
                    print("Group:", contacts[full_name]['group'])
                    found = True
            if not found:
                print("Contact not found.")
        else:
            print("Invalid search type.")
    
    elif choice == "3":
        name = input("Enter full name of contact to update: ")
        if name in contacts:
            print("Update:")
            print("1. Phone")
            print("2. Email")
            print("3. Address")
            print("4. Group")
            field = input("Choose what to update: ")

            if field == "1":
                new_phone = input("Enter new phone: ")
                contacts[name]["phone"] = new_phone
                print("Phone updated successfully!")
            elif field == "2":
                new_email = input("Enter new email: ")
                contacts[name]["email"] = new_email
                print("Email updated successfully!")
            elif field == "3":
                new_address = input("Enter new address: ")
                contacts[name]["address"] = new_address
                print("Address updated successfully!")
            elif field == "4":
                new_group = input("Enter new group: ")
                contacts[name]["group"] = new_group
                print("Group updated successfully!")
            else:
                print("Invalid field.")
        else:
            print("Contact not found.")
    elif choice == "4":
        name = input("Enter full name of contact to delete: ")
        if name in contacts:
            del contacts[name]
            print("Contact deleted.")
        else:
            print("Contact not found.")
    elif choice == "5":
        if contacts:
            for name, value in contacts.items():
                print(f"\nName: {name}")
                for k, v in value.items():
                    print(f"{k}: {v}")
                print("----------------")
        else:
            print("No contacts available.")
    elif choice == "6":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Choose between 1-6.")


                    
