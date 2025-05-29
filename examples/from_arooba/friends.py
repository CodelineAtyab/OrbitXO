# Dictionary to store user and their friends
friend_data = {}
running= True
while running:
    print("\nFriends List Comparison Tool")
    print("1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")

    choose= input("Choose an option: ")
    if choose == "1":
        print("1. Add user and friends\n")

        name = input("Enter user name: ")
        friends = input("Enter friends (comma-separated): ")
        friend_set = set(friend.strip() for friend in friends.split(","))
        friend_data[name] = friend_set
        print(f"{name}'s friends list saved.\n")
        print("User added.")


    elif choose == "2":
        print("2. Find mutual friends\n")
        name1 = input("Enter first user: ")
        name2 = input("Enter second user: ")

        if name1 in friend_data and name2 in friend_data:
         mutual = friend_data[name1] & friend_data[name2]
         print("Mutual friends:", mutual)
        else:
            print("One or both users not found.")

 
    elif choose == "3":
        print("3. Find unique friends")

        user1 = input("Enter first user: ")
        user2 = input("Enter second user: ")
        if user1 in friend_data and user2 in friend_data:
            only_user1 = friend_data[user1] - friend_data[user2]
            only_user2 = friend_data[user2] - friend_data[user1]
            print(f"Friends only {user1} has:", only_user1)
            print(f"Friends only {user2} has:", only_user2, "\n")
        else:
         print("One or both users not found.\n")

    elif choose == "4":
        print("4. Combine all friends")

        user1 = input("Enter first user: ")
        user2 = input("Enter second user: ")
        if user1 in friend_data and user2 in friend_data:
            combined = friend_data[user1] | friend_data[user2]
            print("Combined friends:", combined, "\n")
        else:
            print("One or both users not found.\n")

    elif choose == "5":
        print("5. Get friend suggestions")

        user = input("Get friend suggestions for: ")
        if user not in friend_data:
            print("User not found.\n")
            False 
        
        suggestions = set() 
        user_friends = friend_data[user]
        for friend in user_friends:
            if friend in friend_data:
                suggestions |= (friend_data[friend] - user_friends - {user})
                print("Suggested friends:", suggestions, "\n")

    elif choose == "6":
        running= False
        print("6. Exit, Goodbye =) !!!!!!!!!")

    else:
        print("Invalid option.")
    


