import csv
import json
all_contacts = {}
while True:
  print("Contact Book System")
  print("1. Add Contact")
  print("2. Search Contacts")
  print("3. Update Contact")
  print("4. Delete Contact")
  print("5. View All Contacts and Sort")
  print("6. Manage Groups")
  print("7. Import/Export Contacts")
  print("8. Exit")

  input_choice = input("Choose an option: ")
  if input_choice == '1':
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    name = first_name + " " + last_name
    phone = input("Phone: ")
    email = input("Email: ")
    address = input("Address: ")
    group = input("Group (work/family/friends/other): ")
    all_contacts[name] = {'phone': phone, 'email': email, 'address': address, 'group': group}
    print(f"Contact {name} added successfully.")

  elif input_choice == '2':
    print("Search by: 1. Name 2. Phone 3. Email 4. Group")
    search_choice = input("Choose search type: ")
    if search_choice == '1':
      input_name = input("Enter your contact name: ")
      if input_name in all_contacts:
        print(f"Contact found: {input_name}: {all_contacts[input_name]}")
      else:
        print("Contact not found.")
    elif search_choice == '2':
      input_phone = input("Enter phone number: ")
      found = True
      for name, details in all_contacts.items():
        if details['phone'] == input_phone:
          print(f"Contact found: {name}: {details}")
          break
        else:  
          found = False
          print("Contact not found.")
    elif search_choice == '3':
        input_email = input("Enter email: ")
        found = True
        for name, details in all_contacts.items():
          if details['email'] == input_email:
            print(f"Contact found: {name}: {details}")
            break
          else:
            found = False
            print("Contact not found.")
    elif search_choice == '4':
        input_group = input("Enter group (work/family/friends/other): ")
        found = True
        for name, details in all_contacts.items():
          if details['group'] == input_group:
            print(f"Contact found: {name}: {details}")
            break
          else:
            found = False
            print("Contact not found.")
    else:
        print("Invalid search type. Please try again.")

  elif input_choice == '3':
    name = input("Enter contact name to update: ")
    if name in all_contacts:
      print("Select field to update: ")
      print("1. Phone")
      print("2. Email")
      print("3. Address")
      print("4. Group")
      input_field = input("Choose field to update: ")
      if input_field == '1':
        print("Current phone number: ", all_contacts[name]['phone'])
        new_phone = input("Enter new phone number: ")
        all_contacts[name]['phone'] = new_phone
        print(f"Contact {name} updated successfully.")
      elif input_field == '2':
        print("Current email: ", all_contacts[name]['email'])
        new_email = input("Enter new email: ")
        all_contacts[name]['email'] = new_email
        print(f"Contact {name} updated successfully.")
      elif input_field == '3':
        print("Current address: ", all_contacts[name]['address'])
        new_address = input("Enter new address: ")
        all_contacts[name]['address'] = new_address
        print(f"Contact {name} updated successfully.")
      elif input_field == '4':
        print("Current group: ", all_contacts[name]['group'])
        new_group = input("Enter new group (work/family/friends/other): ")
        all_contacts[name]['group'] = new_group
        print(f"Contact {name} updated successfully.")
      else:
        print("Invalid field. Please try again.")
    else:
      print("Contact not found.")

  elif input_choice == '4':
    name = input("Enter contact name to delete: ")
    if name in all_contacts:
      del all_contacts[name]
      print(f"Contact {name} deleted successfully.")
    else:
      print("Contact not found.")

  elif input_choice == '5':
    print ("View all contacts and sort by: 1. first name 2. last name 3. group")
    sort_choice = input("Choose sorting type: ")
    if sort_choice == '1':
        contacts_list = list(all_contacts.items())
        n = len(contacts_list)
        for i in range(n):
            for j in range(0, n-i-1):
                name1 = contacts_list[j][0].split()[0]
                name2 = contacts_list[j+1][0].split()[0]
                if name1 > name2:
                    contacts_list[j], contacts_list[j+1] = contacts_list[j+1], contacts_list[j]
        
        print("Contacts sorted by first name:")
        for name, details in contacts_list:
            print(f"{name}: {details}")
    elif sort_choice == '2':
        contacts_list = list(all_contacts.items())
        n = len(contacts_list)
        for i in range(n):
            for j in range(0, n-i-1):
                name1 = contacts_list[j][0].split()[-1]
                name2 = contacts_list[j+1][0].split()[-1]
                if name1 > name2:
                    contacts_list[j], contacts_list[j+1] = contacts_list[j+1], contacts_list[j]
        
        print("Contacts sorted by last name:")
        for name, details in contacts_list:
            print(f"{name}: {details}")
    elif sort_choice == '3':
        contacts_list = list(all_contacts.items())
        n = len(contacts_list)
        for i in range(n):
            for j in range(0, n-i-1):
                group1 = contacts_list[j][1]['group']
                group2 = contacts_list[j+1][1]['group']
                if group1 > group2:
                    contacts_list[j], contacts_list[j+1] = contacts_list[j+1], contacts_list[j]
        
        print("Contacts sorted by group:")
        for name, details in contacts_list:
            print(f"{name}: {details}")
    else: 
        print("Invalid sorting type. Please try again.")

  elif input_choice == '6':
    print("Group Management")
    print("1. Create Group")
    print("2. Add Contacts to Group")
    print("3. Remove Contacts from Group")  
    input_group_choice = input("Choose group management option: ")
    if input_group_choice == '1':
      group_name = input("Enter group name: ")
      all_contacts[group_name] = []
      print(f"Group {group_name} created successfully.")
    elif input_group_choice == '2':
      group_name = input("Enter group name: ")
      if group_name in all_contacts:
        contact_name = input("Enter contact name to add: ")
        if contact_name in all_contacts:
          all_contacts[group_name].append(contact_name)
          print(f"Contact {contact_name} added to group {group_name}.")
        else:
          print("Contact not found.")
      else:
        print("Group not found.")
    elif input_group_choice == '3':
      group_name = input("Enter group name: ")
      if group_name in all_contacts:
        contact_name = input("Enter contact name to remove: ")
        if contact_name in all_contacts[group_name]:
          all_contacts[group_name].remove(contact_name)
          print(f"Contact {contact_name} removed from group {group_name}.")
        else:
          print("Contact not found in the group.")
      else:
        print("Group not found.")
    else:
      print("Invalid group management option. Please try again.")

  elif input_choice == '7':
    print("Import/Export Contacts")
    print("1. Import Contacts")
    print("2. Export Contacts")
    input_import_export = input("Choose import/export option: ")
    if input_import_export == '1':
      file_name = input("Enter file name to import from: ")
      print("Import format: ")
      print("1. CSV")
      print("2. JSON")
      input_import_format = input("Choose import format: ")
      if input_import_format == '1':
        with open(file_name, 'r') as csvfile:
          reader = csv.DictReader(csvfile)
          for row in reader:
            name = row['Name']
            phone = row['Phone']
            email = row['Email']
            address = row['Address']
            group = row['Group']
            all_contacts[name] = {'phone': phone, 'email': email, 'address': address, 'group': group}
          csvfile.close()
        print(f"Contacts imported from {file_name} in CSV format...")   
      if input_import_format == '2':
        with open(file_name, 'r') as jsonfile:
          all_contacts = json.load(jsonfile)
          jsonfile.close()
          print(f"Contacts imported from {file_name} in JSON format...")
      else:
        print("Invalid import format. Please try again.")
      print(f"Importing contacts from {file_name}...")
    elif input_import_export == '2':
      print("Export format: ")
      print("1. CSV") 
      print("2. JSON")
      input_export_format = input("Choose export format: ")
      if input_export_format == '1':
        file_name = input("Enter file name to export to (must end with .csv): ")
        with open(file_name, 'w', newline='') as csvfile:
          fieldnames = ['Name', 'Phone', 'Email', 'Address', 'Group']
          writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
          writer.writeheader()
          for name, details in all_contacts.items():
            writer.writerow({'Name': name, 'Phone': details['phone'], 'Email': details['email'], 'Address': details['address'], 'Group': details['group']})
        csvfile.close()
        print(f"Exporting contacts to {file_name} in CSV format...")
      elif input_export_format == '2':
        file_name = input("Enter file name to export to (must end with .json): ")
        print(f"Exporting contacts to {file_name} in JSON format...")
        with open(file_name, 'w') as jsonfile:
          json.dump(all_contacts, jsonfile, indent=4)
        jsonfile.close()
        print(f"Contacts exported to {file_name} in JSON format.")
      else:
        print("Invalid export format. Please try again.")
    else:
      print("Invalid import/export option. Please try again.")

  elif input_choice == '8':
    break
  else:
    print("Invalid choice. Please try again.")
