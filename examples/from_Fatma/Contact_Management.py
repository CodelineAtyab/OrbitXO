import datetime
contacts = []
print ("\nContact Book System")
print ("Last updated: " , datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
while True:
     
     #User: CodelineAtyab
     print("\n1. Add Contact")
     print("2. Search Contact")
     print("3. Update Contact")
     print("4. Delete Contact")
     print("5. Exit")

     choice = int(input("\nChoose an option: "))

    # Add contact
     if choice == 1:
        print("Enter contact details: ")

        first= input ("First name: ")
        last = input ("Last name: ")
        phone = input ("Phone: ")
        email = input ("Email: ")
        address = input ("Address: ")
        group = input ("Group (work/family/friends/other): ")

        contact = {"first":first, "last":last, "phone": phone, "email": email, "address": address, "group":group}
        contacts.append(contact)

        print ("Contact added successfully!")

# Search Contact
     elif choice == 2:

        print("Search by: ")
        print ("1. Name ")
        print ("2. Phone ")
        print ("3. Email")
        print ("4. Group")

        search = int (input ("Choose search type: "))

        target = "" 
        results =[]
        if search == 1:
            target = input ("Enter name: ") .lower()
            for c in contacts:
                full_name =(c["first"]+ " "+ c["last"]).lower()
                if target in full_name:
                   results.append(c)

        elif search == 2:
            target = input ("Enter phone: ")
            for c in contacts:
                if target in c["phone"]:
                   results.append(c)      

        elif search == 3:
            target = input ("Enter email: ").lower()
            for c in contacts:
                if target in c["email"].lower():
                   results.append(c)   

        elif search == 4:
            target = input ("Enter group: ").lower()
            for c in contacts:
                if target in c["group"].lower():
                   results.append(c)         

        else:
            print("Invalid search")           

        if results:
            print(f"Found {len(results)} contact: \n")     
            for c in results:
                print("Name: ", c["first"], c["last"])           
                print("Phone: ", c["phone"])
                print("Email: ", c["email"])
                print("Address: ", c["address"])
                print("Group: ", c["group"]) 
                print()
        else:        
            print("No contact found")


# Update Contact
     elif choice == 3:
         name = input("Enter contact name to update: ")
         found = False
         if c in contacts:
             full_name = (c["first"] + " " + c["last"]).lower()
             if name == full_name:
                 found = True
                 print("Select field to update: ")
                 print("1. Phone")
                 print("2. Email")
                 print("3. Address")
                 print("4. Group")

                 choose = int (input("Choose field: "))

                 if choose == 1:
                     print("Current phone: " , c["phone"])
                     c["phone"] = input ("Enter new phone: ")
                 elif choose == 2: 
                     print("Current email: " , c["email"])   
                     c["email"] = input ("Enter new email: ")
                 elif choose == 3: 
                     print("Current address: " , c["address"])   
                     c["address"] = input ("Enter new address: ")
                 elif choose == 4: 
                     print("Current group: " , c["group"])   
                     c["group"] = input ("Enter new group: ")
                 else:
                     print("Invalid input")
                     break
                 print("Contact updated successfully!")
                 break
             if not found:
                 print("contact not found.")

# Delete Contac 
     elif choice == 4:
         name = input ("Enter contact name to delete ")
         delete = False
         for i in range(len(contacts)):
             full_name = (contacts[i]["first"] + " " + contacts[i]["last"]).lower()
             if name == full_name:
                 confirm = input(f"Are you sure you want to delete {name}? (y/n): ").lower()
                 if confirm == "y":
                     del contacts[i]
                     delete = True
                     print("Contact deleted successfully")
                 else:
                     ("Deletion canceled")
                 break        
         if not delete:
             print("Contact not found")

# Exit
     elif choice == 5:
       print(" Thank you!")
       break

     else:
       print("invalid input")