users = {}
main_menu = True

while main_menu:
    print("Friend list Comparison Tool")
    print("1. Add user and Friend")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        user_name = input("Enter user name: ")
        friends_input = input("Enter friends separated by a comma: ")
        friends = set(friend.strip() for friend in friends_input.split(","))
        users[user_name] = friends
        print(f"User and friends added: {users}\n")

    elif choice == "2":
        user_1 = input("Enter first user: ")
        user_2 = input("Enter second user: ")
        if user_1 in users and user_2 in users:
            mutual = users[user_1] & users[user_2]
            print(f"Mutual friends: {mutual}\n")
        else:
            print("No mutual friends found.\n")

    elif choice == "3":
        user_1 = input("Enter first user: ")
        user_2 = input("Enter second user: ")
        if user_1 in users and user_2 in users:
            only_user_1 = users[user_1] - users[user_2]
            only_user_2 = users[user_2] - users[user_1]
            print(f"Unique friends for {user_1}: {only_user_1}")
            print(f"Unique friends for {user_2}: {only_user_2}\n")
        else:
            print("No unique friends found.\n")

    elif choice == "4":
        user_1 = input("Enter first user: ")
        user_2 = input("Enter second user: ")
        if user_1 in users and user_2 in users:
            combined = users[user_1] | users[user_2]
            print(f"Combined friends: {combined}\n")
        else:
            print("One or both users not found.\n")

    elif choice == "5":
        user_1 = input("Enter first user: ")
        user_2 = input("Enter second user: ")
        if user_1 in users and user_2 in users:
            user_2_unique = users[user_2] - users[user_1]
            print(f"Friend suggestions for {user_1}: {user_2_unique}\n")
        else:
            print("No suggestion for friends were found.\n")

    elif choice == "6":
        print("Exiting...")
        main_menu = False

    else:
        print("Invalid option. Please try again.\n")
