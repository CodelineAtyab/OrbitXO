
users = {}

def add_user():
    name = input("Enter user name: ")
    friends_input = input("Enter friends (comma-separated): ")
    friends_list = friends_input.split(",")
    friends_set = set()
    
    for friend in friends_list:
        if friend != "":
            friends_set.add(friend)
    
    users[name] = friends_set
    print(name + "'s friends added.\n")


def find_mutual_friends():
    user1 = input("Enter first user: ")
    user2 = input("Enter second user: ")

    if user1 in users and user2 in users:
        mutual = users[user1] & users[user2]
        print("Mutual friends:", mutual, "\n")
    else:
        print("One or both users not found.\n")


def find_unique_friends():
    user1 = input("Enter first user: ")
    user2 = input("Enter second user: ")

    if user1 in users and user2 in users:
        only_user1 = users[user1] - users[user2]
        only_user2 = users[user2] - users[user1]
        print("Friends only " + user1 + " has:", only_user1)
        print("Friends only " + user2 + " has:", only_user2)
        print("")
    else:
        print("One or both users not found.\n")


def combine_friends():
    user1 = input("Enter first user: ")
    user2 = input("Enter second user: ")

    if user1 in users and user2 in users:
        all_friends = users[user1] | users[user2]
        print("All friends from both users:", all_friends, "\n")
    else:
        print("One or both users not found.\n")


def suggest_friends():
    name = input("Get friend suggestions for: ")

    if name not in users:
        print("User not found.\n")
        return

    suggestions = set()

    for friend in users[name]:
        if friend in users:
            suggestions = suggestions | users[friend]
    
    suggestions = suggestions - users[name]

    if name in suggestions:
        suggestions.remove(name)

    print("Suggested friends:", suggestions, "\n")


def main():
    while True:
        print("Friends List Comparison Tool")
        print("1. Add user and friends")
        print("2. Find mutual friends")
        print("3. Find unique friends")
        print("4. Combine all friends")
        print("5. Get friend suggestions")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_user()
        elif choice == "2":
            find_mutual_friends()
        elif choice == "3":
            find_unique_friends()
        elif choice == "4":
            combine_friends()
        elif choice == "5":
            suggest_friends()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.\n")

# Start the program
main()
