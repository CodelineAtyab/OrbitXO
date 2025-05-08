
contacts={}

print("Contact Book System")

while True:
    print("\n1.Add Contact")
    print("2.Search Contact")
    print("3.Update Contact")
    print("4.Delete Contact")
    print("5.List All Contacts") #optional 
    print("6.Manage Groups")  #optional 
    print("7.Import/Export Contacts")   #optional 
    print("8.Exit")

    option=input("Choose an option: ")

#option 1
    if option=="1":
        print("\nEnter contact details:")
        first_name=input("First name: ").title() #to capitalizes the first letter
        last_name=input("Last name: ").title()
        full_name=first_name + " " + last_name  #combine first and last name to create key for full name

        if full_name not in contacts:
            phone=input("Phone: ")
            email=input("Email: ")
            address=input("Address: ")
            group=input("Group (work/family/friends/other): ")
            contacts[full_name]= {   #store new contact in the dictionary using full name as the key for the dictionary
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "email": email,
                "address": address,
                "group": group
            }
            print("\nContact added successfyly!")

        else:
            print("Contact already exist!")

#option 2
    elif option=="2":
        print("Search by: ")
        print("1.Name")
        print("2.Phone")
        print("3.Email")
        print("4.Group")
        search_type=input("choose search type: ")

        results=[]  #start with an empty list to store the matched results

        if search_type=="1":
            name=input("Enter name: ") 
            for key, info in contacts.items():  #Loop through each contact in contacts dictionary
                full_name=info["first_name"] + " " + info["last_name"]
                if name in full_name:
                    results.append(info)  #add matching contacts to the results list


        elif search_type=="2":
            phone=input("Enter phone: ")
            for info in contacts.values():
                if info["phone"]==phone:
                    results.append(info) #add matching contact


        elif search_type=="3":
            email=input("Enter email: ")
            for info in contacts.values():
                if info["email"]==email:
                    results.append(info)


        elif search_type=="4":
            email=input("Enter group: ")
            for info in contacts.values():
                if info["group"]==group:
                    results.append(info)

        else:
            print("Invalid search type.")  #for options other than 1-4

#to isplay results if any contacts found        
        if len(results)>0:
            print(f"\nFound the {len(results)} contact(s):")
            for info in results:
                print(f"\nName: {info['first_name']} {info['last_name']}")
                print(f"Phone: {info['phone']}")
                print(f"Email: {info['email']}")
                print(f"Address: {info['address']}")
                print(f"Group: {info['group']}")
        else:
            print("No contacts found.")

#option 3
    elif option=="3":
        name=input("Enter contact name to update: ")
        if name in contacts:
            print("\nSelect field to update: \n1.Phone \n2.Email \n3.Address \n4.Group")

            update_selected=input("Choose field: ")

            if update_selected=="1":
                print(f"Current phone: {contacts[name]['phone']}")
                contacts[name]['phone'] = input("Enter new phone: ")
                print("Phone updated successfully!")

            elif option=="2":
                print(f"Current email: {contacts[name]['email']}")
                contacts[name]['email'] = input("Enter new email: ")
                print("Email updated successfully!")

            elif option=="3":
                print(f"Current address: {contacts[name]['address']}")
                contacts[name]['address'] = input("Enter new address: ")
                print("Address updated successfully!")

            elif option=="4":
                print(f"Current group: {contacts[name]['group']}")
                contacts[name]['group'] = input("Enter new group: ")
                print("Group updated successfully!")

            else:
                print("Invalid selection.")

#option 4
    elif option == '4':
        name=input("Enter contact name to delete: ")
        if name in contacts:
            del contacts[name]  #use del statement to remove the contact from the dictionary
            print("Contact deleted successfully!")
        else:
            print("\nContact not found.")

#option 8
    elif option=='8':
        print("Exiting the Contacts!")
        break

#for the options other than 1-8
    else:
        print("Invalid option. Please try again.")

