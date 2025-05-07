users = {}

while True:
    print("\nFriends List Comparison Tool")
    print("1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")

    choice = input("Choose an option: ").strip()

    if choice == '1':
        user = input("Enter user name: ").strip()
        friends_input = input("Enter friends (comma-separated): ").strip()
        friends = set(( split(","), friends_input.split(',')))
        users[user] = friends
        print(f"Added {user} with friends: {users[user]}")

    elif choice == '2':
        u1 = input("Enter first user: ").strip()
        u2 = input("Enter second user: ").strip()
        if u1 in users and u2 in users:
            mutual = users[u1] & users[u2]
            print(f"Mutual friends: {mutual}")
        else:
            print("One or both users not found.")

    elif choice == '3':
        u1 = input("Enter first user: ").strip()
        u2 = input("Enter second user: ").strip()
        if u1 in users and u2 in users:
            only_u1 = users[u1] - users[u2]
            only_u2 = users[u2] - users[u1]
            print(f"Friends only {u1} has: {only_u1}")
            print(f"Friends only {u2} has: {only_u2}")
        else:
            print("One or both users not found.")

    elif choice == '4':
        u1 = input("Enter first user: ").strip()
        u2 = input("Enter second user: ").strip()
        if u1 in users and u2 in users:
            combined = users[u1] | users[u2]
            print(f"All friends combined: {combined}")
        else:
            print("One or both users not found.")

    elif choice == '5':
        user = input("Get friend suggestions for: ").strip()
        if user in users:
            suggestions = set()
            for friend in users[user]:
                if friend in users:
                    suggestions |= users[friend]
            suggestions -= users[user]
            suggestions.discard(user)
            print(f"Suggested friends: {suggestions}")
        else:
            print("User not found.")

    elif choice == '6':
        print("Exiting...")
        break

    else:
        print("Invalid choice. Try again.")
