import json

cbook = {}

while True:
    print("""               
Contact Book System
1. Add Contact
2. Search Contact
3. Update Contact
4. Delete Contact
5. Sorting Cotacts
6. Export Contacts
7. Exit
    """)
    choice = input("Choose an option: ")

    if choice == "1":
        print("Enter contact details:")
        fname = input("First name: ")
        lname = input("Last name: ")
        phone = input("Phone: ")
        email = input("Email: ")
        addr = input("Address: ")
        group = input("Group (work/family/friends/other): ").lower()

        key = f"{fname.lower()} {lname.lower()}"

        if key in cbook:
            print("Contact already exists!")
        else:
            data = {
                "first_name": fname,
                "last_name": lname,
                "phone": phone,
                "email": email,
                "address": addr,
                "group": group
            }
            cbook[key] = data
            print("Contact added successfully!")

    elif choice == "2":
        print("""Search by:
1. Name
2. Phone
3. Email
4. Group""")
        s_type = input("Choose search type: ")

        s_val = input("Enter search value: ").lower()
        found = False

        for info in cbook.values():
            if (s_type == "1" and (s_val in info['first_name'].lower() and s_val in info['last_name'].lower())) or \
               (s_type == "2" and s_val in info['phone'].lower()) or \
               (s_type == "3" and s_val in info['email'].lower()) or \
               (s_type == "4" and s_val == info['group'].lower()):
                print(f"""
Name: {info['first_name']} {info['last_name']}
Phone: {info['phone']}
Email: {info['email']}
Address: {info['address']}
Group: {info['group'].capitalize()}
""")
                found = True

        if not found:
            print("No matching contact found.")

    elif choice == "3":
        name_key = input("Enter contact full name to update: ").lower()

        if name_key not in cbook:
            print("Contact not found.")
        else:
            info = cbook[name_key]
            print("""Select field to update:
1. Phone
2. Email
3. Address
4. Group""")
            field = input("Choose field: ")

            if field == "1":
                print(f"Current phone: {info['phone']}")
                info['phone'] = input("Enter new phone: ")
            elif field == "2":
                print(f"Current email: {info['email']}")
                info['email'] = input("Enter new email: ")
            elif field == "3":
                print(f"Current address: {info['address']}")
                info['address'] = input("Enter new address: ")
            elif field == "4":
                print(f"Current group: {info['group']}")
                info['group'] = input("Enter new group: ").lower()
            else:
                print("Invalid choice.")

            print("Contact updated successfully!")

    elif choice == "4":
        del_key = input("Enter contact full name to delete: ").lower()

        if del_key in cbook:
            del cbook[del_key]
            print("Contact deleted successfully!")
        else:
            print("Contact not found.")

    elif choice == "5":
        if not cbook:
            print("No contacts available.")
        else:
            print("""Sort by:
1. First name
2. Last name
3. Group""")
            sort = input("Choose sorting: ")

            contact_list = list(cbook.values())
            sorted_list = []

            if sort == "1":
                for contact in contact_list:
                    sorted_list.append((contact['first_name'].lower(), contact))
            elif sort == "2":
                for contact in contact_list:
                    sorted_list.append((contact['last_name'].lower(), contact))
            elif sort == "3":
                for contact in contact_list:
                    sorted_list.append((contact['group'].lower(), contact))
            else:
                sorted_list = [(0, contact) for contact in contact_list]

            sorted_list.sort()

            cur_grp = ""
            for key, info in sorted_list:
                if sort == "3" and info['group'] != cur_grp:
                    cur_grp = info['group']
                    print(f"\n{cur_grp.upper()}:")
                print(f"- {info['first_name']} {info['last_name']} ({info['phone']})")

    elif choice == "6":
        with open("contacts.json", "w") as file:
            json.dump(cbook, file, indent=4)
        print("Contacts exported to contacts.json successfully!")

    elif choice == "7":
        print("Exiting Contact Book.")
        break

    else:
        print("Invalid option, please try again.")
