contacts = {}


while True:
        print("\nContact Book System")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. List All Contact")
        print("6. Exit") 

        choice = input("Choose an option: ")

        if choice == '1':
           first_name = input ("Fisrt name: ")
           last_name = input("Last name: ")
           full_name = first_name + " " + last_name

           if full_name in contacts:
               print("Contact already exists.")
           else: 
               phone = input("Phone: ")
               email = input("Email: ")
               address = input ("Address: ")
               group = input("Group (work/family/friends/others):") 

               contacts [full_name] = {
                    'phone': phone,
                    'email':email,
                    'address': address, 
                    'group':group
              }
               print("Contact added successfully")

        elif choice =='2': 

            print("Search by:")
            print("1. Name")
            print("2. Phone")
            print("3. Email")
            print("4. Group")
            search_type = input("Choose search type: ")

            if search_type == '1':
                name_input = input("Enter name: ") 
                for name in contacts: 
                    if name_input.lower() in name.lower():
                        print("\nName:", name)
                        print("Phone:", contacts[name]['phone'])
                        print("Email:", contacts[name]['email'])
                        print("Address:", contacts[name]['address'])
                        print("Group:", contacts[name]['group'])

            elif search_type == '2':
                phone_input = input("Enter phone: ")
                for name in contacts: 
                    if phone_input == contacts[name]['phone']:
                       print("\nName:", name)
                       print("Phone:", contacts[name]['phone'])
                       print("Email:", contacts[name]['email'])
                       print("Address:", contacts[name]['address'])
                       print("Group:", contacts[name]['group'])   

            elif search_type == '3':
                email_input = input("Enter email: ")
                for name in contacts:
                    if email_input == contacts[name]['email']:
                       print("\nName:", name)
                       print("Phone:", contacts[name]['phone'])
                       print("Email:", contacts[name]['email'])
                       print("Address:", contacts[name]['address'])
                       print("Group:", contacts[name]['group'])

            elif search_type == '4':
                group_input = input("Enter group: ").lower()
                for name in contacts: 
                    if group_input == contacts[name]['group']:
                        print("\nName:", name)
                        print("Phone:", contacts[name]['phone'])
                        print("Email:", contacts[name]['email'])
                        print("Address:", contacts[name]['address'])
                        print("Group:", contacts[name]['group'])

            else: 
                print("Invalid search type.")



        elif choice == '3': 
            name_to_update = input("Enter contact name to Update: ")
            if name_to_update in contacts:
               print("Select field to update:")
               print("1. Phone")
               print("2. Email")
               print("3. Address")
               print("4. Group") 
               field_choice = input("Choose field: ")

               if field_choice == '1': 
                   new_phone = input("Enter new phone: ")
                   contacts[name_to_update]['phone'] = new_phone

               elif field_choice == '2':
                   new_email = input("Enter new email: ")
                   contacts[name_to_update]['email'] = new_email

               elif field_choice == '3':
                   new_address = input("Enter new address: ")
                   contacts[name_to_update]['address'] = new_address

               elif field_choice == '4':
                   new_group = input("Enter new group: ")
                   contacts[name_to_update]['group'] = new_group 

               else: 
                   print ("Invalid field.")
               print("Contact updated successfully")   
            else: 
                print("Contact not found. ")


        elif choice == '4':
            name_to_delete = input("Enter contact name to delete: ")
            if name_to_delete in contacts:
                del contacts[name_to_delete] 
                print("Contact deleted.")
            else:
                print("Contact not found.")


        elif choice == '5':
            if not contacts: 
                print("No contacts to display.")
            else: 
                print("Sort by: ")
                print("1. First name")
                print("2. Last name")
                print("3. Group")
                sort_option = input("Choose sorting: ") 

                contact_list = list(contacts.items())

                # Function to get first name
                def get_first_name(contact):
                     return contact[0].split()[0]

                # Function to get last name
                def get_last_name(contact):
                     return contact[0].split()[-1]
 
                # Function to get group
                def get_group(contact):
                     return contact[1]['group']

                if sort_option == '1':
                    contact_list.sort(key=get_first_name)
                elif sort_option == '2':
                    contact_list.sort(key=get_last_name)
                elif sort_option == '3':
                     contact_list.sort(key=get_group)
                else:
                     print("Invalid sort option. Showing unsorted.")

                for name, info in contact_list:
                    print("\nName:", name)
                    print("Phone:", info['phone'])
                    print("Email:", info['email'])
                    print("Address:", info['address'])
                    print("Group:", info['group'])

        elif choice == '6':
             print("Goodbye")
             break

        else:
             print("Invalid choice. Please try again.")       