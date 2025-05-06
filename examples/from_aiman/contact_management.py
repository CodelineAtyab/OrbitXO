contact_book = {}
while True:
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. List All Contacts")
    print("6. Exit")
    user_option = input("Choose an option: ")
    
    if user_option == "1":
        print("Enter Contact details:")
        fname = input("First Name: ")
        lname = input("Last Name: ")
        full_name = fname + " " + lname
        mobile = input("Phone: ")
        mail = input("Email: ")
        location = input("Address: ")
        category = input("Work/Family/Friends/Other: ")
        if mobile in contact_book:
            print("Error: This phone number already exists!")
        else:
            contact_book[mobile] = {
                'name': full_name,
                'phone': mobile,
                'email': mail,
                'address': location,
                'groups': category
            }
            print("Contact added successfully!")

    elif user_option == "2":
        print("Search by:")
        print("1. Name")
        print("2. Phone")
        print("3. Email")
        print("4. Group")
        search_option = input("Choose a Search type: ")
        contact_found = False

        if search_option == "1":
            search_name = input("Enter first name and last name: ")
            for mobile, details in contact_book.items():
                if details['name'] == search_name:
                    print(f"Contact found: {mobile} : {details}")
                    contact_found = True
                    break
            if not contact_found:
                print("Contact not found")

        elif search_option == "2":
            search_mobile = input("Enter a phone number: ")
            if search_mobile in contact_book:
                print(f"Contact found: {search_mobile} : {contact_book[search_mobile]}")
                contact_found = True
            else:
                print("Contact not found")

        elif search_option == "3":
            search_email = input("Enter your Email: ")
            for mobile, details in contact_book.items():
                if details['email'] == search_email:
                    print(f"Contact found: {mobile} : {details}")
                    contact_found = True
                    break
            if not contact_found:
                print("Contact not found")

        elif search_option == "4":
            search_group = input("Enter your Group: ")
            for mobile, details in contact_book.items():
                if details['groups'] == search_group:
                    print(f"Contact found: {mobile} : {details}")
                    contact_found = True
            if not contact_found:
                print("Contact not found")

    elif user_option == "3":
        update_contact_name = input("Enter first name and last name of contact to update: ")
        found_number = None
        for mobile, details in contact_book.items():
            if details['name'] == update_contact_name:
                found_number = mobile
                break
        if found_number is None:
            print("Contact not found.")
        else:
            print("1. Phone")
            print("2. Email")
            print("3. Address")
            print("4. Groups")
            update_field = input("Select field to update: ")

            if update_field == "1":
                updated_mobile = input("Enter the new phone number: ")
                if updated_mobile in contact_book and updated_mobile != found_number:
                    print("Error: This phone number is already assigned to another contact.")
                else:
                    temp_data = contact_book[found_number].copy()
                    temp_data['phone'] = updated_mobile
                    contact_book[updated_mobile] = temp_data
                    del contact_book[found_number]
                    print("Phone number updated successfully!")

            elif update_field == "2":
                updated_email = input("Enter new email: ")
                contact_book[found_number]['email'] = updated_email
                print("Email updated successfully!")

            elif update_field == "3":
                updated_address = input("Enter new address: ")
                contact_book[found_number]['address'] = updated_address
                print("Address updated successfully!")

            elif update_field == "4":
                updated_group = input("Enter new Group (Work/Family/Friends/Other): ")
                contact_book[found_number]['groups'] = updated_group
                print("Group updated successfully!")

    elif user_option == "4":
        print("Remove Contact")
        delete_name = input("Enter the first name and last name of the contact to delete: ")
        phone_to_delete = None
        for mobile, details in contact_book.items():
            if details['name'] == delete_name:
                phone_to_delete = mobile
                break
        if phone_to_delete:
            del contact_book[phone_to_delete]
            print(f"Contact '{delete_name}' has been removed successfully.")
        else:
            print("Contact not found.")

    elif user_option == "5":
        print("List all the Contacts")
        if not contact_book:
            print("No contacts found.")
        else:
            for mobile, details in contact_book.items():
                print(f"Name: {details['name']}")
                print(f"Phone: {details['phone']}")
                print(f"Email: {details['email']}")
                print(f"Address: {details['address']}")
                print(f"Group: {details['groups']}")
                print("-" * 30)

    elif user_option == "6":
        print("Contact Book closed. Have a great day!")
        break

    else:
        print("Invalid option. Please try again.")