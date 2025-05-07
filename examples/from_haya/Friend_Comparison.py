friend_net = {}
while True:
    print("\nFriends List Comparison Tool")
    print("1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")

    menu_choice = input("Choose an option: ").strip()

    if menu_choice == '1':
        username = input("Enter user name: ").strip()
        friends_input = input("Enter friends : ")
        friends_set = set(friend.strip() for friend in friends_input.split(",") if friend.strip()) 
        friend_net[username] = friends_set
        print(f"{username} friends added: {friends_set}")

    elif menu_choice == '2':
        user_a = input("Enter first user: ").strip() 
        user_b = input("Enter second user: ").strip()
        if user_a in friend_net and user_b in friend_net:
            mutual_friends = friend_net[user_a] & friend_net[user_b]
            print(f"Mutual friends: {mutual_friends if mutual_friends else 'None'}")
        else:
            print("One or both users not found.")

    elif menu_choice == '3':
        user_a = input("Enter first user: ").strip()
        user_b = input("Enter second user: ").strip()
        if user_a in friend_net and user_b in friend_net:
            unique_to_a = friend_net[user_a] - friend_net[user_b]
            unique_to_b = friend_net[user_b] - friend_net[user_a]
            print(f"Friends only {user_a} has: {unique_to_a if unique_to_a else 'None'}")
            print(f"Friends only {user_b} has: {unique_to_b if unique_to_b else 'None'}")
        else:
            print("One or both users not found.")

    elif menu_choice == '4':
        user_a = input("Enter first user: ").strip()
        user_b = input("Enter second user: ").strip()
        if user_a in friend_net and user_b in friend_net:
            all_friends = friend_net[user_a] | friend_net[user_b]
            print(f"All friends of {user_a} and {user_b}: {all_friends}")
        else:
            print("One or both users not found.")

    elif menu_choice == '5':
        target_user = input("Get friend suggestions for: ").strip()
        if target_user not in friend_net:
            print("User not found.")
        else:
            suggestion_pool = set()
            for do in friend_net[target_user]:
                if do in friend_net:
                    suggestion_pool |= (friend_net[do] - friend_net[target_user] - {target_user})
            print(f"Suggested friends: {suggestion_pool if suggestion_pool else 'None'}")

    elif menu_choice == '6':
        print("Exit")
        break

    else:
        print("Invalid option.")
