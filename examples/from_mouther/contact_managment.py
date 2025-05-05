import csv
import json

all_contacts = {}

while True:
    print("\nContact Book System")
    print("1. Add Contact")
    print("2. Search Contacts")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. View All Contacts and Sort")
    print("6. Manage Groups")
    print("7. Import/Export Contacts")
    print("8. Exit")

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
        print("Sort by: 1. First Name 2. Last Name 3. Group")
        sort_choice = input("Choose sorting type: ")

        sorted_contacts = list(all_contacts.items())
        #This code is mainly ai generated (the lambda function) but I understood it 100% 
        #as in it creates a samll  anonymous function for the purpos of that singular line
        if sort_choice == '1':
            sorted_contacts.sort(key=lambda x: x[0].split()[0])
        elif sort_choice == '2':
            sorted_contacts.sort(key=lambda x: x[0].split()[-1])
        elif sort_choice == '3':
            sorted_contacts.sort(key=lambda x: x[1]['group'])
        else:
            print("Invalid sort choice.")
            continue

        for name, details in sorted_contacts:
            print(f"{name}: {details}")

    elif choice == '6':
        print("Group Management")
        print("1. View Group Members")
        input_group_choice = input("Choose option: ")

        if input_group_choice == '1':
            group_name = input("Enter group name: ")
            found = False
            for name, details in all_contacts.items():
                if details['group'] == group_name:
                    print(f"{name}: {details}")
                    found = True
            if not found:
                print("No contacts in this group.")


    elif choice == '7':
        #This choice was a combination of ai, myself and tariq's help
        print("1. Import Contacts\n2. Export Contacts")
        io_choice = input("Choose option: ")

        if io_choice == '1':
            file_name = input("Enter file name to import from: ")
            format_choice = input("Format (1. CSV, 2. JSON): ")
            try:
                if format_choice == '1':
                    with open(file_name, 'r') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            name = row['Name']
                            all_contacts[name] = {
                                'phone': row['Phone'],
                                'email': row['Email'],
                                'address': row['Address'],
                                'group': row['Group']
                            }
                    print("CSV import successful.")
                elif format_choice == '2':
                    with open(file_name, 'r') as f:
                        all_contacts.update(json.load(f))
                    print("JSON import successful.")
                else:
                    print("Invalid format.")
            except:
                print("Import failed. Check your file.")

        elif io_choice == '2':
            file_name = input("Enter file name to export to: ")
            format_choice = input("Format (1. CSV, 2. JSON): ")
            try:
                if format_choice == '1':
                    with open(file_name, 'w', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=['Name', 'Phone', 'Email', 'Address', 'Group'])
                        writer.writeheader()
                        for name, d in all_contacts.items():
                            writer.writerow({'Name': name, 'Phone': d['phone'], 'Email': d['email'], 'Address': d['address'], 'Group': d['group']})
                    print("CSV export successful.")
                elif format_choice == '2':
                    with open(file_name, 'w') as f:
                        json.dump(all_contacts, f, indent=4)
                    print("JSON export successful.")
                else:
                    print("Invalid format.")
            except:
                print("Export failed.")

    elif choice == '8':
        print("Exiting Contact Book. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
