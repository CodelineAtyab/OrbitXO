import json

cbook = {}

while True:
    print("\nContact Book System")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. List All Contacts")
    print("6. Export Contacts")
    print("7. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        # Adding a contact
        print("\nEnter contact details:")
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
            cbook[key] = {
                "first_name": fname,
                "last_name": lname,
                "phone": phone,
                "email": email,
                "address": addr,
                "group": group
            }
            print("Contact added successfully!")

    elif choice == "2":
        # Searching for a contact
        print("\nEnter the full name to search: ")
        search = input().lower()
        
        if search in cbook:
            contact = cbook[search]
            print(f"\nName: {contact['first_name']} {contact['last_name']}")
            print(f"Phone: {contact['phone']}")
            print(f"Email: {contact['email']}")
            print(f"Address: {contact['address']}")
            print(f"Group: {contact['group']}")
        else:
            print("Contact not found.")

    elif choice == "3":
        # Updating a contact
        print("\nEnter full name to update: ")
        name_key = input().lower()
        
        if name_key in cbook:
            print("Enter what to update (phone/email/address/group): ")
            field = input().lower()
            
            if field in cbook[name_key]:
                print(f"Enter new {field}: ")
                new_value = input()
                cbook[name_key][field] = new_value
                print("Contact updated successfully!")
            else:
                print("Invalid field.")
        else:
            print("Contact not found.")

    elif choice == "4":
        # Deleting a contact
        print("\nEnter full name to delete: ")
        name_key = input().lower()
        
        if name_key in cbook:
            del cbook[name_key]
            print("Contact deleted successfully!")
        else:
            print("Contact not found.")

    elif choice == "5":
        # Listing all contacts
        if not cbook:
            print("\nNo contacts available.")
        else:
            print("\nList of contacts:")
            for name, details in cbook.items():
                print(f"\n{name.title()}: {details['phone']} | {details['email']} | {details['address']} | {details['group']}")

    elif choice == "6":
        # Exporting contacts to a file
        with open("contacts.json", "w") as file:
            json.dump(cbook, file, indent=4)
        print("\nContacts exported successfully!")

    elif choice == "7":
        # Exit
        print("\nGoodbye!")
        break

    else:
        print("\nInvalid option. Please try again.")