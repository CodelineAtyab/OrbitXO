Users ={}

main_menu = True

while main_menu:
    print("Friend list Comparison Tool")
    print("1. Add user and Friend")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combaine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")

   
    menu= True

    choice= input("Choose an option: ")
    while menu:
        if choice == '1':
            print("Add user and Friend.")
            user = input("Enter user name: ")
            friend = input("Enter friend (comma-separated): ")
            friends = []
            friends = friend.split(",")

            if user in Users:
                print("User already exists. Adding friend to existing user.")
                Users[user].extend(friends)

            else:
                print("Adding new user and friend.")
                Users[user] = []
            Users[user].append(friends)
            print("User and friend added successfully.")
            print("Friend set: ", friends)
            print("All users: ", Users[user])

            break
        
        elif choice == '2':
            print("Find mutual friends.")
            user1 = input("Enter first user: ")
            user2 = input("Enter second user: ")
            user1_sets = set()
            user2_sets = set()
            for friends in Users[user1]:
                user1_sets = user1_sets | set(friends)

            for friends in Users[user2]:
                user2_sets = user2_sets | set(friends)
            mutual_friends = user1_sets & user2_sets

            if  mutual_friends :
             print("Mutual friends: ", mutual_friends)

            break
        
        elif choice == '3':
            print("Find unique friends.")
            user1 = input("Enter first user: ")
            user2 = input("Enter second user: ")
            user1_sets = set()
            user2_sets = set()
            for friends in Users[user1]:
                user1_sets = user1_sets | set(friends)

            for friends in Users[user2]:
                user2_sets = user2_sets | set(friends)
            unique_friends = user1_sets - user2_sets

            if  unique_friends:
             print("Unique friends: ", unique_friends)

            break
        
        elif choice == '4':
            print("Combine all friends.")
            user1 = input("Enter first user: ")
            user2 = input("Enter second user: ")
            user1_sets = set()
            user2_sets = set()
            for friends in Users[user1]:
                user1_sets = user1_sets | set(friends)

            for friends in Users[user2]:
                user2_sets = user2_sets | set(friends)
            combined_friends = user1_sets | user2_sets

            if combined_friends:
             print("Combined friends: ", combined_friends)

            break
        
        elif choice == '5':
            print("Get friend suggestions.")
            user = input("Enter user: ")
            user_sets = set()
            suggestions = set()
            for friends in Users[user]:
             user_sets = user_sets | set(friends)

            for other_user, friends in Users.items():
             
             if other_user != user:
              other_user_sets = set()

              for friends in friends:
               other_user_sets = other_user_sets | set(friends)
               mutual_friends = user_sets & other_user_sets

               if mutual_friends:
                suggestions.add(other_user)
                suggestions.update(other_user_sets - user_sets)

            if  suggestions:
                print("Friend suggestions:", suggestions)

            break
        
        elif choice == '6':
            print("Exiting the program.")
            main_menu = False

            break
        else:
           print("Invalid option try again.")
           