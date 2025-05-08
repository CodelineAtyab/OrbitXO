import time

# Main contact storage
contacts = {}

# Helper: format full name
def get_full_name(first, last):
    return f"{first.strip().title()} {last.strip().title()}"

# Add contact
def add_contact():
    print("Enter contact details:")
    first = input("First name: ")
    last = input("Last name: ")
    full_name = get_full_name(first, last)
    
    if full_name in contacts:
        print("Contact already exists!")
        return
    
    phone = input("Phone: ")
    email = input("Email: ")
    address = input("Address: ")
    group = input("Group (work/family/friends/other): ").lower()
    
    contacts[full_name] = {
        "phone": phone,
        "email": email,
        "address": address,
        "group": group
    }
    
    print("Contact added successfully!")

# Search contact
def search_contact():
    print("Search by:\n1. Name\n2. Phone\n3. Email\n4. Group")
    choice = input("Choose search type: ")
    query = input("Enter search term: ").lower()
    
    found = False
    for name, info in contacts.items():
        if (choice == "1" and query in name.lower()) or \
           (choice == "2" and query in info["phone"]) or \
           (choice == "3" and query in info["email"].lower()) or \
           (choice == "4" and query == info["group"]):
            print(f"\nName: {name}")
            print(f"Phone: {info['phone']}")
            print(f"Email: {info['email']}")
            print(f"Address: {info['address']}")
            print(f"Group: {info['group'].upper()}")
            found = True
    if not found:
        print("No matching contact found.")

# Update contact
def update_contact():
    name = input("Enter contact name to update: ").title()
    if name not in contacts:
        print("Contact not found.")
        return

    print("Select field to update:\n1. Phone\n2. Email\n3. Address\n4. Group")
    field = input("Choose field: ")
    fields = {"1": "phone", "2": "email", "3": "address", "4": "group"}

    if field in fields:
        current = contacts[name][fields[field]]
        new_val = input(f"Current {fields[field]}: {current}\nEnter new {fields[field]}: ")
        contacts[name][fields[field]] = new_val
        print("Contact updated successfully!")
    else:
        print("Invalid choice.")

# Delete contact
def delete_contact():
    name = input("Enter contact name to delete: ").title()
    if name in contacts:
        del contacts[name]
        print("Contact deleted.")
    else:
        print("Contact not found.")

# List contacts
def list_contacts():
    if not contacts:
        print("No contacts to display.")
        return

    print("Sort by:\n1. First name\n2. Last name\n3. Group")
    sort_option = input("Choose sorting: ")

    def sort_key(item):
        name = item[0]
        if sort_option == "1":
            return name.split()[0]
        elif sort_option == "2":
            return name.split()[-1]
        elif sort_option == "3":
            return item[1].get("group", "")
        return name

    sorted_contacts = sorted(contacts.items(), key=sort_key)

    print("\nContacts:")
    for name, info in sorted_contacts:
        print(f"- {name} ({info['phone']})")

# Placeholder for future features
def manage_groups():
    print("Group management not implemented yet.")

def import_export_contacts():
    print("Import/Export not implemented yet.")

# ----- PROGRAM STARTS HERE -----
print("Contact Book System")
print("Last updated:", time.strftime("%Y-%m-%d %H:%M:%S"))

while True:
    print("\n1. Add Contact\n2. Search Contact\n3. Update Contact\n4. Delete Contact\n"
          "5. List All Contacts\n6. Manage Groups\n7. Import/Export Contacts\n8. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        add_contact()
    elif choice == "2":
        search_contact()
    elif choice == "3":
        update_contact()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        list_contacts()
    elif choice == "6":
        manage_groups()
    elif choice == "7":
        import_export_contacts()
    elif choice == "8":
        print("Goodbye!")
        break
    else:
        print("Invalid option. Try again.")
