contact_list = {}

while True:
    print("Contact Book System")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. Exit")

    x = input("Select an option: ")

    if x == "1":
        print("Enter Contact Details: ")
        your_name = input("Enter first name: ")
        family_name = input("Enter last name: ")
        Name = your_name + " " + family_name
        phone = input("Phone: ")
        email = input("Email: ")
        address = input("Address: ")
        groups = input("Family/Friends/Work/Others: ")
        contact_list[Name] ={'phone' : phone, 'email' : email, 'address' : address, 'group' : groups }
        print("Contact Added Successfully")

    elif x == "2":
        print("Search by:")
        print("1. Name")
        print("2. phone")
        print("3. Email")
        print("4. Group")

        Search_with = input("Select a search by: ")

        if Search_with == "1":
            full_name = input("Enter your first name and last: ")

            if full_name in contact_list:
                print(f"Contact found : {full_name}: {contact_list[full_name]}")

            else:
                print("Contact are not found")
        
        elif Search_with == "2":
            phone_number = input("Enter a phone number: ")

            for phone, customer_informations in contact_list.items():
             if customer_informations['phone'] == phone_number:
                 print(f"Contact found {phone} : {customer_informations}")

             else:
                print("Contact are not found")
            
        
        elif Search_with == "3":
            input_email = input("Enter your Email: ")
            for phone, customer_emails in contact_list.items():
             
             if customer_emails['email'] == input_email:
                 print(f"Contact found {phone} : {customer_emails}")

            else:
                print("Contact are not found")
            
        elif Search_with == "4":
            input_groups = input("Enter your Group: ")

            for phone, customer_groups in contact_list.items():
             if customer_groups['group'] == input_groups:
                 print(f"Contact found {phone} : {customer_groups}")

            else:
                print("Contact are not found")

    elif x == "3":
            customers_update = input("Enter Your first name and last name: ")
            print("1. Phone")
            print("2. Email")
            print("3. Address")
            print("4. Groups ")
            
            choice = input ("Select field to update:")

            if choice == "1":
                input_phone = input("Enter the new phone number: ")
                contact_list[customers_update]['phone'] = input_phone
                print("the updated phone number: ", input_phone)
            
            elif choice == "2":
                input_email = input("Enter ur updated email: ")
                contact_list[customers_update]['email'] = input_email
                print("the updated  email : ", input_email)

            elif choice == "3":
                input_address = input("Enter ur updated address: ")
                contact_list[customers_update]['address'] = input_address
                print("the updated address: ", input_address)


            elif choice == "4":
                input_groups = input("Enter ur updated Group: ")
                contact_list[customers_update]['groups'] = input_groups
                print("the updated group: ", input_groups)

    elif  x == "4":
             
             print("Remove Contact")
             input_name = input("Enter the first name and last name of the contact to be deleted: ")

             if input_name in contact_list:
                contact_list.pop(input_name)
                print(f"Contact name : {input_name} has been removed")

    elif  x == "5":
             print("please try again")
             break
    else:
        print("Exit")

             
