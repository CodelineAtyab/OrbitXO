all_contacts = {}
while True:
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. List All Contacts")
    print("6. Manage Groups")
    print("7. Import/Export Contacts")
    print("8. Exit")

    a = input("Choose an option: ")

    if a == "1":
        print("Enter Contact details:")
        first_name = input("First Name: ")
        secound_name = input("Last Name: ")
        name = first_name + " " + secound_name
        phone = input("Phone: ")
        email = input("Email: ")
        Address = input("Address: ")
        groups = input("Work/Family/Friends/Other: ")
        all_contacts[phone] = {'phone' : phone, 'email' : email , 'Address' : Address , 'groups' : groups}
        print("Contact added successfully!")

    elif a == "2":
        print("Search by:")
        print("1. Name")
        print("2. Phone")
        print("3. Email")
        print("4. Group")

        Search_by = input("Choose a Search type: ")

        if Search_by == "1":
            input_name = input("Enter your first name and last name: ")
            if input_name in all_contacts:
                print(f"Contact found : {input_name}: {all_contacts[input_name]}")
            else:
                print("Contact not found")
        
        elif Search_by == "2":
            input_phone = input("Enter a phone number: ")
            for phone, customer_details in all_contacts.items():
             if customer_details['phone'] == input_phone:
                 print(f"Contact found {phone} : {customer_details}")
             else:
                print("Contact not found")
            
        
        elif Search_by == "3":
            input_email = input("Enter your Email: ")
            for phone, customer_emails in all_contacts.items():
             if customer_emails['email'] == input_email:
                 print(f"Contact found {phone} : {customer_emails}")
            else:
                print("Contact not found")
            
        elif Search_by == "4":
            input_groups = input("Enter your Group: ")
            for phone, customer_groups in all_contacts.items():
             if customer_groups['groups'] == input_groups:
                 print(f"Contact found {phone} : {customer_groups}")
            else:
                print("Contact not found")

    elif a == "3":
            update_customer = input("Enter Your first name and last name: ")
            print("1. Phone")
            print("2. Email")
            print("3. Address")
            print("4. Groups ")
            customer_choice = input ("Select field to update:")
            if customer_choice == "1":
                input_phone = input("Enter the new phone number: ")
                all_contacts[update_customer]['phone'] = input_phone
                print("the updated phone number: ", input_phone)
            
            elif customer_choice == "2":
                input_email = input("Enter ur updated email: ")
                all_contacts[update_customer]['email'] = input_email
                print("the updated  email : ", input_email)

            elif customer_choice == "3":
                input_address = input("Enter ur updated address: ")
                all_contacts[update_customer]['address'] = input_address
                print("the updated address: ", input_address)


            elif customer_choice == "4":
                input_groups = input("Enter ur updated Group: ")
                all_contacts[update_customer]['groups'] = input_groups
                print("the updated group: ", input_groups)

    elif  a == "4":
             print("Remove Contact")
             input_name = input("Enter the first name and last name of the contact to be deleted: ")

             if input_name in all_contacts:
                all_contacts.pop(input_name)
                print(f"Contact name : {input_name} has been removed")

    elif a == "5":
        print("List all the Contacts")
        for key, value in all_contacts.items():
            print(key, value)



            

           
        



