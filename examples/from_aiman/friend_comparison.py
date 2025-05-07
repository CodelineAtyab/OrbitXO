user_data = {}
is_main_menu_active = True

while is_main_menu_active:
    print("Friend List Comparison Tool")
    print("1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")

    keep_in_submenu = True
    option = input("Choose an option: ")

    while keep_in_submenu:
        if option == '1':
            print("Add user and friends.")
            username = input("Enter user name: ")
            input_friends = input("Enter friends (comma-separated): ").split(",")
            if username in user_data:
                print("User already exists. Adding friends to existing user.")
                user_data[username].extend(input_friends)
            else:
                print("Adding new user and friends.")
                user_data[username] = input_friends
            print("Friend list added successfully.")
            print("Friend set:", input_friends)
            print("All users:", user_data[username])
            break

        elif option == '2':
            print("Find mutual friends.")
            user_one = input("Enter first user: ")
            user_two = input("Enter second user: ")
            friends_one = set(user for sublist in user_data[user_one] for user in [sublist])
            friends_two = set(user for sublist in user_data[user_two] for user in [sublist])
            shared_friends = friends_one & friends_two
            if shared_friends:
                print("Mutual friends:", shared_friends)
            break

        elif option == '3':
            print("Find unique friends.")
            first_user = input("Enter first user: ")
            second_user = input("Enter second user: ")
            first_set = set(user for sublist in user_data[first_user] for user in [sublist])
            second_set = set(user for sublist in user_data[second_user] for user in [sublist])
            unique_to_first = first_set - second_set
            if unique_to_first:
                print("Unique friends:", unique_to_first)
            break

        elif option == '4':
            print("Combine all friends.")
            name1 = input("Enter first user: ")
            name2 = input("Enter second user: ")
            set1 = set(user for sublist in user_data[name1] for user in [sublist])
            set2 = set(user for sublist in user_data[name2] for user in [sublist])
            all_friends = set1 | set2
            if all_friends:
                print("Combined friends:", all_friends)
            break

        elif option == '5':
            print("Get friend suggestions.")
            current_user = input("Enter user: ")
            current_friends = set(user for sublist in user_data[current_user] for user in [sublist])
            recommendations = set()

            for other, friend_list in user_data.items():
                if other != current_user:
                    other_set = set(friend for sublist in friend_list for friend in [sublist])
                    if current_friends & other_set:
                        recommendations.add(other)
                        recommendations.update(other_set - current_friends)

            if recommendations:
                print("Friend suggestions:", recommendations)
            break

        elif option == '6':
            print("Exiting the program.")
            is_main_menu_active = False
            break

        else:
            print("Invalid option. Please try again.")
