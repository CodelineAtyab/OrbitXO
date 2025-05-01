while True:
    print("Frinds List Comparison Tool")
    print("1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")


    user_friends = {} #dictonary 

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
                first_name = input("Enter first user: ")
                secound_name = input("Enter Secound user: ")
                first_name_set = set()
                secound_name_set = set()
                for friend_list in user_friends[first_name]:
                      first_name_set = first_name_set | set(friend_list)
                for friend_list in user_friends[secound_name]:
                      secound_name_set = secound_name_set | set(friend_list)

                mutual_friends = first_name_set & secound_name_set
                print("Mutual friends: ", mutual_friends )
            

