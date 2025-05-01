users = {}

def add_user():
    user_name = input("Enter user name: ").strip()
    friends_input = input("Enter friends sperat friends by a coma: ")
    # Split the input string by commas and strip whitespace from each friend name
    friends = set(friend.strip() for friend in friends_input.split(","))
    users[user_name] = friends
    return users

def find_mutual_friends():
    user_1 = input("Enter first user: ").strip()
    user_2 = input("Enter second user: ").strip()
    if user_1 in users and user_2 in users:
        mutual = users[user_1] & users[user_2]
        print(f"Mutual friends: {mutual}\n")
        return mutual
    else:
        print("No mutual friends found.\n")

def find_unique_friends():
    user_1 = input("Enter first user: ").strip()
    user_2 = input("Enter second user: ").strip()
    if user_1 in users and user_2 in users:
        only_user_1 = users[user_1] - users[user_2]
        only_user_2 = users[user_2] - users[user_1]
        return only_user_1, only_user_2
    else:
        print("No unique friends found.\n")

def combine_all_friends():
    u1 = input("Enter first user: ").strip()
    u2 = input("Enter second user: ").strip()
    if u1 in users and u2 in users:
        combined = users[u1] | users[u2]
        return combined
    else:
        print("One or both users not found.\n")

def suggest_friends():
    unique_friends = find_unique_friends()
    if unique_friends != "":
        user_1, user_2 = unique_friends
        suggested_friends = user_2
        return suggested_friends
    else:
        print("No suggestion for friends were found.\n")


main_menu = True
while main_menu:
    print("Friend list Comparison Tool")
    print("1. Add user and Friend")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combaine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")


    menu = True

    x = input("Choose an option: ")
    while menu:
        if x == "1":
            user_friend_list = add_user()
            print(f"User and friends added: {user_friend_list}\n")
            break
        elif x == "2":
            mutual_friends = find_mutual_friends()
            print(f"Mutual friends found {mutual_friends}\n")
            break
        elif x == "3":
            unique_friends = find_unique_friends()
            print(f"Unique friends found {unique_friends}\n")
            break
        elif x == "4":
            combined_friends = combine_all_friends()
            print(f"Combined friends found {combined_friends}\n")
            break
        elif x == "5":
            suggested = suggest_friends()
            print(f"Friend suggestions found {suggested}\n")
            break
        elif x == "6":
            print("Exiting...")
            menu = False
            main_menu = False
        else:
            print("Invalid option. Please try again.")
            menu = False
