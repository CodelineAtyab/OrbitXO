contacts = {}

running = True
while running:
    print("\nContact Menu")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. List All Contacts")
    print("6. Exit")

    choice = input("Choose an option (1-6): ")

    if choice == '1':
        print("\nAdd Contact")
        first_name = input("First name: ")
        last_name = input("Last name: ")
        name_key = first_name.strip().title() + " " + last_name.strip().title()

        if name_key in contacts:
            print("Contact already exists!")
        else:
            phone = input("Phone: ")
            email = input("Email: ")
            address = input("Address: ")
            group = input("Group (work/family/friends/other): ").lower()

            contacts[name_key] = {
                "phone": phone,
                "email": email,
                "address": address,
                "group": group
            }
            print("Contact added successfully.")

    elif choice == '2':
        print("\nSearch Contact")
        print("1. By Name")
        print("2. By Phone")
        print("3. By Email")
        print("4. By Group")

        search_option = input("Choose an option: ")
        found = False

        if search_option == '1':
            name = input("Enter name: ").strip().title()
            for key in contacts:
                if name in key:
                    print(f"\nName: {key}")
                    print(f"Phone: {contacts[key]['phone']}")
                    print(f"Email: {contacts[key]['email']}")
                    print(f"Address: {contacts[key]['address']}")
                    print(f"Group: {contacts[key]['group']}")
                    found = True
        elif search_option == '2':
            phone = input("Enter phone: ")
            for key in contacts:
                if contacts[key]['phone'] == phone:
                    print(f"\nName: {key}")
                    print(f"Phone: {contacts[key]['phone']}")
                    print(f"Email: {contacts[key]['email']}")
                    print(f"Address: {contacts[key]['address']}")
                    print(f"Group: {contacts[key]['group']}")
                    found = True
        elif search_option == '3':
            email = input("Enter email: ")
            for key in contacts:
                if contacts[key]['email'] == email:
                    print(f"\nName: {key}")
                    print(f"Phone: {contacts[key]['phone']}")
                    print(f"Email: {contacts[key]['email']}")
                    print(f"Address: {contacts[key]['address']}")
                    print(f"Group: {contacts[key]['group']}")
                    found = True
        elif search_option == '4':
            group = input("Enter group: ").lower()
            for key in contacts:
                if contacts[key]['group'] == group:
                    print(f"\nName: {key}")
                    print(f"Phone: {contacts[key]['phone']}")
                    print(f"Email: {contacts[key]['email']}")
                    print(f"Address: {contacts[key]['address']}")
                    print(f"Group: {contacts[key]['group']}")
                    found = True
        else:
            print("Invalid search option.")

        if not found:
            print("No contact found.")

    elif choice == '3':
        print("\nUpdate Contact")
        name = input("Enter full name to update: ").strip().title()

        if name in contacts:
            print("1. Phone")
            print("2. Email")
            print("3. Address")
            print("4. Group")
            update_option = input("Choose what to update: ")

            if update_option == '1':
                new_phone = input("Enter new phone: ")
                contacts[name]['phone'] = new_phone
            elif update_option == '2':
                new_email = input("Enter new email: ")
                contacts[name]['email'] = new_email
            elif update_option == '3':
                new_address = input("Enter new address: ")
                contacts[name]['address'] = new_address
            elif update_option == '4':
                new_group = input("Enter new group: ")
                contacts[name]['group'] = new_group.lower()
            else:
                print("Invalid option.")
            print("Contact updated successfully.")
        else:
            print("Contact not found.")

    elif choice == '4':
        print("\nDelete Contact")
        name = input("Enter full name to delete: ").strip().title()

        if name in contacts:
            del contacts[name]
            print("Contact deleted.")
        else:
            print("Contact not found.")

    elif choice == '5':
        print("\nAll Contacts")
        if len(contacts) == 0:
            print("No contacts to show.")
        else:
            for key in sorted(contacts):
                print(f"\nName: {key}")
                print(f"Phone: {contacts[key]['phone']}")
                print(f"Email: {contacts[key]['email']}")
                print(f"Address: {contacts[key]['address']}")
                print(f"Group: {contacts[key]['group']}")

    elif choice == '6':
        print("Goodbye!")
        running = False

    else:
        print("Invalid choice. Please try again.")