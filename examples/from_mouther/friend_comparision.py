users = {}

def add_user():
    user_name = input("Enter user name: ").strip()
    friends_input = input("Enter friends sperat friends by a coma: ")
    # Split the input string by commas and strip whitespace from each friend name
    friends = set(friend.strip() for friend in friends_input.split(","))
    users[user_name] = friends

def find_mutual_friends():
    user_1 = input("Enter first user: ").strip()
    user_2 = input("Enter second user: ").strip()
    if user_1 in users and user_2 in users:
        mutual = users[user_1] & users[user_2]
        print(f"Mutual friends: {mutual}\n")
    else:
        print("One or both users not found.\n")

