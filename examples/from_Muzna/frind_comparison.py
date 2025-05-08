frind_dict ={}

while True:
    print("\nFriends List Comparison Tool")
    print("1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")

    choice = input("Choose an option: ")

    if choice == '1':
        user = input("Enter user name: ").strip()
        friends_name = input("Enter friends: ")
        friend_list = [name.strip() for name in friends_name.split(",")]

        if user in frind_dict:
            frind_dict[user].update(friend_list)
        else:
            frind_dict[user] = set(friend_list)

        print(f"User {user} added with friends: {frind_dict[user]}")

    elif choice == '2':
        print()
        user1 = input("Enter first user: ").strip()
        user2 = input("Enter second user: ").strip()

        if user1 in frind_dict and user2 in frind_dict:
            mutual = frind_dict[user1] & frind_dict[user2]
            if mutual:
                print(f"Mutual friends between {user1} and {user2}: {mutual}")
            else:
                print("No mutual friends.")
        else:
            print("One or both users not found.")        

    elif choice == '3':
        print()
        user1 = input("Enter first user: ").strip()
        user2 = input("Enter second user: ").strip()
        if user1 in frind_dict and user2 in frind_dict:
            only_user1 = frind_dict[user1] - frind_dict[user2]
            only_user2 = frind_dict[user2] - frind_dict[user1]

            print(f"\nFriends only {user1} : {only_user1 if only_user1 else 'None'}")
            print(f"Friends only {user2} : {only_user2 if only_user2 else 'None'}")
        else:
            print("One or both users not found.")

    elif choice == '4':
        print()
        user1 = input("Enter first user: ").strip()
        user2 = input("Enter second user: ").strip()

        if user1 in frind_dict and user2 in frind_dict:
            all_friends = frind_dict[user1] | frind_dict[user2]
            print(f"\nAll friends of {user1} and {user2}: {all_friends}")
        else:
            print("One or both users not found.")

    elif choice == '5':
        print()
        user = input("Enter user name for suggestions: ").strip()
        if user in frind_dict:
            suggestions = set()
            current_friends = frind_dict[user]

            for friend in current_friends:
                if friend in frind_dict:
                    suggestions.update(frind_dict[friend])

            
            suggestions -= current_friends
            suggestions.discard(user)

            if suggestions:
                print(f"Suggested friends for {user}: {suggestions}")
            else:
                print("No new suggestions available.")
        else:
            print("User not found.")

    elif choice == '6':
        print("see you!")
        break
    else:
        print("Invalid option. Choose between 1-6.")