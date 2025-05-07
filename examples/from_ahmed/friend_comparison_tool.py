user_friends = {}

while True:
    print("\nFriends List Comparison Tool")
    print("1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")

    option = input("Choose an option: ")

    if option == "1":
        name = input("Enter user name: ")
        friends_input = input("Enter friends (comma-separated): ")
        friends = friends_input.split(",")

        if name in user_friends:
            print("User already exists, adding new friends.")
            user_friends[name].extend(friends)
        else:
            print("Creating new user and adding friends.")
            user_friends[name] = friends

        print("Current friends for", name, ":", user_friends[name])

    elif option == "2":
        u1 = input("Enter first user: ")
        u2 = input("Enter second user: ")
        if u1 in user_friends and u2 in user_friends:
            f1 = set(user_friends[u1])
            f2 = set(user_friends[u2])
            print("Mutual friends:", f1 & f2)

    elif option == "3":
        u1 = input("Enter first user: ")
        u2 = input("Enter second user: ")
        if u1 in user_friends and u2 in user_friends:
            f1 = set(user_friends[u1])
            f2 = set(user_friends[u2])
            print("Friends only", u1, "has:", f1 - f2)
            print("Friends only", u2, "has:", f2 - f1)

    elif option == "4":
        u1 = input("Enter first user: ")
        u2 = input("Enter second user: ")
        if u1 in user_friends and u2 in user_friends:
            f1 = set(user_friends[u1])
            f2 = set(user_friends[u2])
            print("All combined friends:", f1 | f2)

    elif option == "5":
        name = input("Enter your name: ")
        if name in user_friends:
            own_friends = set(user_friends[name])
            suggestions = set()
            for other, other_friends in user_friends.items():
                if other != name:
                    other_set = set(other_friends)
                    if own_friends & other_set:
                        suggestions |= other_set - own_friends
            print("Friend suggestions for", name, ":", suggestions)

    elif option == "6":
        print("Goodbye!")
        break