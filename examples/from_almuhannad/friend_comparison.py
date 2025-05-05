user_friends = {} #dictonary
while True:
      print("Frinds List Comparison Tool")
      print("1. Add user and friends")
      print("2. Find mutual friends")
      print("3. Find unique friends")
      print("4. Combine all friends")
      print("5. Get friend suggestions")
      print("6. Exit")
 

      a = input("Choose an option: ")
      if a == "1":
            print("Add user and friends \n")
            entName = input("Enter user name: ") # Entering a username 
            entFriends = input("Enter friends (comma-separated): ") # entering friends (ahmed,ayman,tariq)
            friend_list = [] # create a new list to store the friends name.
            friend_list = entFriends.split(",") #split each name ( ahmed ayman tariq)
            if entName in user_friends:  # it will check if the username is already in the dictonary
                   print("User Already Exists. ")
                   user_friends[entName].extend(friend_list) #extend takes each item in the list and adds it one-by-one to the existing list.
            else:
                   print("Adding new user and friends.")
                   user_friends[entName] = [] # will create an empty list for the username for example user_friends["Ali"] = []
                   user_friends[entName].append(friend_list) #This adds the entire list friend_list as a single item inside the user's list.
                   print("User and friend added successfully.")
                   print("Friend set: ", friend_list)
                   print("All users: ", user_friends[entName])
            
      if a == "2":
                print("Find ur mutual friends")
                first_name = input("Enter first name: ")
                secound_name = input("Enter Secound name: ")
                first_name_set = set()
                secound_name_set = set()
                for friend_list in user_friends[first_name]:
                      first_name_set = first_name_set | set(friend_list)
                for friend_list in user_friends[secound_name]:
                      secound_name_set = secound_name_set | set(friend_list)

                mutual_friends = first_name_set & secound_name_set
                print("Mutual friends: ", mutual_friends )

            
      if a == "3":
                  print("Find ur unique friends")
                  first_name = input("Enter first name: ")
                  secound_name = input("Enter secound name: ")
                  first_name_set = set()
                  secound_name_set = set()
                  for friend_list in user_friends[first_name]:
                        first_name_set = first_name_set| set(friend_list)
                  for friend_list in user_friends[secound_name]:
                        secound_name_set = secound_name_set | set(friend_list)
                  unique_friends = first_name_set - secound_name_set
                  print("Your unique friends are: ", unique_friends)


      if a == "4":
                  print("combine friends")
                  first_name = input("Enter first name: ")
                  secound_name = input("Enter secound name: ")
                  first_name_set = set()
                  secound_name_set = set()
                  for friend_list in user_friends[first_name]:
                        first_name_set = first_name_set | set(friend_list)
                  for friend_list in user_friends[secound_name]:
                        secound_name_set = secound_name_set | set(friend_list)
                  combine_friends = first_name_set | secound_name_set
                  print("Your combine friends are: ", combine_friends)

      if a == "5":
                  print("Friend suggestion")
                  user_name = input("Enter your name: ")
                  user_name_set = set()
                  suggest = set()
                  for friend_list in user_friends[user_name]:
                        user_name_set = user_name_set | set(friend_list)
                        for other_user,friend_lists in user_friends.items():
                              if other_user != user_name:
                                    other_user_set = set()
                                    for friend_list in friend_lists:
                                          other_user_set = other_user_set | set(friend_list)
                                          intercection_users = other_user_set & user_name_set
                                          if intercection_users:
                                                suggest.add(other_user)
                                                suggest.update(other_user_set - user_name_set)
                                                print(f"your suggestion friends : {suggest}" )
                                          else:
                                                print("No Friends to suggest")

      if a == "6":
                  print("Exiting the program")
                  break



                  



            


