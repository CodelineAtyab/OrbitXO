#  store users and their friends as sets
users = {}
def add_user_and_friends():
    name = input("Enter user name: ")
    friends_input = input("Enter friends (comma-separated): ")
    friends_list = friends_input.split(",")

    friends_set = set()
    for friend in friends_list:
        if friend != "" and friend != " ":
            if friend[0] == " ":
                friend = friend[1:]  # remove leading space manually
            friends_set.add(friend)

    users[name] = friends_set
    print("User and friends added!")

# find mutual friends
def find_mutual_friends():
    user1 = input("Enter first user: ")
    user2 = input("Enter second user: ")
    if user1 in users and user2 in users:
        mutual = users[user1] & users[user2]
        print("Mutual friends:", mutual)
    else:
        print("One or both users not found.")

# find unique friends
def find_unique_friends():
    user1 = input("Enter first user: ")
    user2 = input("Enter second user: ")
    if user1 in users and user2 in users:
        only_user1 = users[user1] - users[user2]
        only_user2 = users[user2] - users[user1]
        print("Friends only", user1, "has:", only_user1)
        print("Friends only", user2, "has:", only_user2)
    else:
        print("One or both users not found.")

# combine all friends
def combine_all_friends():
    all_friends = set()
    for friend_set in users.values():
        all_friends = all_friends | friend_set
    print("All unique friends from all users:", all_friends)

# suggest friends based on others' friend lists
def suggest_friends():
    name = input("Get friend suggestions for: ")
    if name not in users:
        print("User not found.")
        return

    user_friends = users[name]
    suggestions = set()

    for other_user in users:
        if other_user != name:
            suggestions = suggestions | (users[other_user] - user_friends)
    if name in suggestions:
        suggestions.remove(name)

    print("Suggested friends:", suggestions)

# Main menu
while True:
    print("\nFriends List Comparison Tool")
    print("1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_user_and_friends()
    elif choice == "2":
        find_mutual_friends()
    elif choice == "3":
        find_unique_friends()
    elif choice == "4":
        combine_all_friends()
    elif choice == "5":
        suggest_friends()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 6.")