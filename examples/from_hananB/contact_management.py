import re

contacts = []

def display(result):
    for dict in result:
        print(f"\nName: {dict["First Name"]+dict["Last Name"]}\nPhone: {dict["Phone"]}\nEmail: {dict["Email"]}\nAddress: {dict["Address"]}\nGroup: {dict["Group"]}\n")
        print("--------------------------------------")

def findContact(Stype):
    field_map = {
        "1": "First Name",
        "2": "Phone",
        "3": "Email",
        "4": "Group"
    }
    if Stype in field_map:
        value = input(f"Enter {field_map[Stype]}: ")
        found = [element for element in contacts if element[field_map[Stype]] == value]
        print(f"Found {len(found)} Contact/s: ")
        display(found)

def updateContact(updateN, field):
    field_map = {
        "1": "Phone",
        "2": "Email",
        "3": "Address",
        "4": "Group"
    }
    if field in field_map:
        for contact in contacts:
            if contact["First Name"] == updateN:
                print(f"Current {field_map[field]}: {contact[field_map[field]]}")
                new_val = input(f"Enter new {field_map[field]}: ")
                contact[field_map[field]] = new_val
                print("Contact Updated Successfully!")


print(f"Contact Book System\n\n1. Add Contact\n2. Search Contact \
      \n3. Update Contact\n4. Delete Contact\n5. List All Contacts\n6. Exit")

option = input("\nChoose an Option: ")
while option != "6":
    if option == "1":
        print("Enter Contact Details:")
        f_name = input("First Name: ")
        if f_name.isalpha():
            pass
        else:
            print("Wrong input!")
        l_name = input("Last Name: ")
        if l_name.isalpha():
            pass
        else:
            print("Wrong input!")
        phone = input("Phone: ")
        if bool(re.match(r"^\d{3}-\d{3}-\d{4}$", phone)):
            pass
        else:
            print("Wrong input!")
        email = input("Email: ")
        address = input("Address: ")
        group = input("Group (work/family/friends/other): ")
        if group in ['work','family','friends','other']:
            pass
        else:
            print("Wrong input!")
        contacts.append({"First Name":f_name, "Last Name": l_name, "Phone": phone, "Email": email,"Address": address,"Group": group})
        print("Contact added successfully!")
    if option == "2":
        print("Search by:\n1. Name\n2. Phone\n3. Email\n4. Group")
        search = input("Choose search type: ")
        if search not in ["1","2","3","4"]:
            print("Invalid Input!")
        else:
            findContact(search)
    if option == "3":
        to_update = input("Enter contact name to update: ")
        print("Select field to update:\n1. Phone\n2. Email\n3. Address\n4. Group")
        field = input("Choose field: ")
        if field not in ["1","2","3","4"]:
            print("Invalid Input!")
        else:
            updateContact(to_update,field)
    if option == "4":
        to_delete = input("Enter contact name to delete: ")
        for contact in contacts:
            if contact["First Name"] == to_delete:
                contacts.remove(contact)
                print("Contact Deleted Successfully!")
                break
    if option == "5":
        if len(contacts) == 0:
            print("No contacts in your list!")
        else:
            display(contacts)

    option = input("\nChoose an Option: ")
