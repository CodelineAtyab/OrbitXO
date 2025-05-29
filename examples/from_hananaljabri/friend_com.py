users = {}

def add_user():
    username = input("Enter user name: ")
    friends_input = input("Enter friends (comma-separated): ")
    friends_list = friends_input.split(",")
    friends = set()
    for friend in friends_list:
        friends.add(friend.strip())
    users[username] = friends
    print("User and friends added!\n")
#Enter1
def find_mutual_friends():
    user1 = input("Enter first user: ")
    user2 = input("Enter second user: ")
    if user1 in users and user2 in users:
        mutual = users[user1] & users[user2]
        print("Mutual friends:", mutual, "\n")
    else:
        print("User not found.\n")

def find_unique_friends():
    user1 = input("Enter first user: ")
    user2 = input("Enter second user: ")
    if user1 in users and user2 in users:
        only_user1 = users[user1] - users[user2]
        only_user2 = users[user2] - users[user1]
        print(f"Friends only {user1} has:", only_user1)
        print(f"Friends only {user2} has:", only_user2, "\n")
    else:
        print("User not found.\n")

def combine_all_friends():
    user1 = input("Enter first user: ")
    user2 = input("Enter second user: ")
    if user1 in users and user2 in users:
        combined = users[user1] | users[user2]
        print("All friends combined:", combined, "\n")
    else:
        print("User not found.\n")

def suggest_friends():
    username = input("Get friend suggestions for: ")
    if username in users:
        suggestions = set()
        for friend in users[username]:
            if friend in users:
                suggestions.update(users[friend] - users[username] - {username})
        print("Suggested friends:", suggestions, "\n")
    else:
        print("User not found.\n")

while True:
    print("Friends List Comparison Tool")
    print("1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit\n")
    
    choice = input("Choose an option: ")
    
    if choice == "1":
        add_user()
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
        print("Invalid option. Try again.\n")