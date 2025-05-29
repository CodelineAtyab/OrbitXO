contacts = {}

def add_contact():
    name = input("Enter full name: ").strip()
    if name in contacts:
        print(" Contact already exists.")
        return
    phone = input("Phone: ")
    email = input("Email: ")
    address = input("Address: ")
    contacts[name] = {"phone": phone, "email": email, "address": address}
    print(" Contact added.")

def search_contact():
    name = input("Enter name to search: ").strip()
    if name in contacts:
        c = contacts[name]
        print(f"\n{name}\nPhone: {c['phone']}\nEmail: {c['email']}\nAddress: {c['address']}")
    else:
        print(" Contact not found.")

def update_contact():
    name = input("Enter name to update: ").strip()
    if name in contacts:
        print("1. Phone\n2. Email\n3. Address")
        choice = input("Choose field: ")
        if choice == "1":
            contacts[name]["phone"] = input("New phone: ")
        elif choice == "2":
            contacts[name]["email"] = input("New email: ")
        elif choice == "3":
            contacts[name]["address"] = input("New address: ")
        else:
            print(" Invalid choice.")
    else:
        print(" Contact not found.")

def delete_contact():
    name = input("Enter name to delete: ").strip()
    if name in contacts:
        del contacts[name]
        print(" Contact deleted.")
    else:
        print(" Contact not found.")

def list_contacts():
    if not contacts:
        print(" No contacts yet.")
    else:
        for name, info in contacts.items():
            print(f"\n{name} | {info['phone']} | {info['email']} | {info['address']}")

def menu():
    while True:
        print("\n Contact Book")
        print("1. Add\n2. Search\n3. Update\n4. Delete\n5. List All\n6. Exit")
        choice = input("Choose option: ")

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
            print(" Goodbye!")
            break
        else:
            print(" Invalid option.")

menu()
