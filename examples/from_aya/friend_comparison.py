
friend_data = {}

print("Friends List Comparison Tool")

while True:
    print("\n1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        username = input("Enter user name: ").strip()
        friends_input = input("Enter friends (comma-separated): ").strip()
        friends = set(friend.strip() for friend in friends_input.split(",") if friend.strip())
        friend_data[username] = friends
        print(f"User '{username}' and friends added successfully.")

    elif choice == "2":
        user1 = input("Enter first user: ").strip()
        user2 = input("Enter second user: ").strip()
        if user1 in friend_data and user2 in friend_data:
            mutual = friend_data[user1] & friend_data[user2]
            print("Mutual friends:", mutual if mutual else "None")
        else:
            print("One or both users not found.")

    elif choice == "3":
        user1 = input("Enter first user: ").strip()
        user2 = input("Enter second user: ").strip()
        if user1 in friend_data and user2 in friend_data:
            only_user1 = friend_data[user1] - friend_data[user2]
            only_user2 = friend_data[user2] - friend_data[user1]
            print(f"Friends only {user1} has:", only_user1 if only_user1 else "None")
            print(f"Friends only {user2} has:", only_user2 if only_user2 else "None")
        else:
            print("One or both users not found.")

    elif choice == "4":
        user1 = input("Enter first user: ").strip()
        user2 = input("Enter second user: ").strip()
        if user1 in friend_data and user2 in friend_data:
            combined = friend_data[user1] | friend_data[user2]
            print("All friends (union):", combined)
        else:
            print("One or both users not found.")

    elif choice == "5":
        user = input("Get friend suggestions for: ").strip()
        if user not in friend_data:
            print("User not found.")

        suggestions = set()
        user_friends = friend_data[user]
        for friend in user_friends:
            if friend in friend_data:
                suggestions.update(friend_data[friend])
        suggestions -= user_friends
        suggestions.discard(user)  

        print("Suggested friends:", suggestions if suggestions else "No suggestions found.")

    elif choice == "6":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please choose between 1 and 6.")
