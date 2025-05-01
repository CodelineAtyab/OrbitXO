all_friends={}
mainmenu = True
while mainmenu:
    print("Friend list Comparison Tool")
    print("1. Add user and Friend")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combaine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")

   
    menu= True

    x= input("Choose an option: ")
    while menu:
        if x == '1':
            print("Add user and Friend.")
            user = input("Enter user name: ")
            friend = input("Enter friend (comma-separated): ")
            friend_list = []
            friend_list = friend.split(",")
            if user in all_friends:
                print("User already exists. Adding friend to existing user.")
                all_friends[user].extend(friend_list)
            else:
                print("Adding new user and friend.")
                all_friends[user] = []
            all_friends[user].append(friend_list)
            print("User and friend added successfully.")
            print("Friend set: ", friend_list)
            print("All users: ", all_friends[user])
            break
        elif x == '2':
            print("Find mutual friends.")
            user1 = input("Enter first user: ")
            user2 = input("Enter second user: ")
            user1_sets = set()
            user2_sets = set()
            for friend_list in all_friends[user1]:
                user1_sets = user1_sets | set(friend_list)
            for friend_list in all_friends[user2]:
                user2_sets = user2_sets | set(friend_list)
            mutual_friends = user1_sets & user2_sets
            if not mutual_friends :
             print("No mutual friends found.")
            else:
             print("Mutual friends: ", mutual_friends)
            break
        elif x == '3':
            print("Find unique friends.")
            user1 = input("Enter first user: ")
            user2 = input("Enter second user: ")
            user1_sets = set()
            user2_sets = set()
            for friend_list in all_friends[user1]:
                user1_sets = user1_sets | set(friend_list)
            for friend_list in all_friends[user2]:
                user2_sets = user2_sets | set(friend_list)
            unique_friends = user1_sets - user2_sets
            if not unique_friends:
             print("No unique friends found.")
            else:
             print("Unique friends: ", unique_friends)
            break
        elif x == '4':
            print("Combine all friends.")
            user1 = input("Enter first user: ")
            user2 = input("Enter second user: ")
            user1_sets = set()
            user2_sets = set()
            for friend_list in all_friends[user1]:
                user1_sets = user1_sets | set(friend_list)
            for friend_list in all_friends[user2]:
                user2_sets = user2_sets | set(friend_list)
            combined_friends = user1_sets | user2_sets
            if not combined_friends:
             print("No combined friends found.")
            else:
             print("Combined friends: ", combined_friends)
            break
        elif x == '5':
            print("Get friend suggestions.")
            user = input("Enter user: ")
            user_sets = set()
            suggestions = set()
            for friend_list in all_friends[user]:
             user_sets = user_sets | set(friend_list)
            for other_user, friend_lists in all_friends.items():
             if other_user != user:
              other_user_sets = set()
              for friend_list in friend_lists:
               other_user_sets = other_user_sets | set(friend_list)
               mutual_friends = user_sets & other_user_sets
               if mutual_friends:
                suggestions.add(other_user)
                suggestions.update(other_user_sets - user_sets)
            if not suggestions:
                print("No friend suggestions found.")
            else:
                print("Friend suggestions:", suggestions)
            break
        elif x == '6':
            print("Exiting the program.")
            menu = False
            break






