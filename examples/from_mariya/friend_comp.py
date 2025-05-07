users = {}


#1st def function Asks for a username, asks for a list of friends (separated by commas)
#cleans the input and stores the names in a set, andsaves everything in a dictionary for future use
def add_user():
    name = input("Enter user name: ").strip() #strip() to remove extra spaces
    friends_input = input("Enter friends (comma-separated): ").strip()
    friends = set(friend.strip() for friend in friends_input.split(",") if friend.strip())
    users[name] = friends
    print(f" Friends added for {name}.")


#2nd def function ask for two users ti enter names.
#If both exist, compare their friends and show the ones they have in common.
def find_mutual_friends():
    u1 = input("Enter first user: ").strip()
    u2 = input("Enter second user: ").strip()
    if u1 in users and u2 in users:
        mutual = users[u1] & users[u2]
        print(" Mutual friends:", mutual)
    else:
        print(" One or both users not found.")


#3rd def function It compares two users and shows the friends that only belong to each person,
# ot the ones they both share.
def find_unique_friends():
    u1 = input("Enter first user: ").strip()
    u2 = input("Enter second user: ").strip()
    if u1 in users and u2 in users:
        only_u1 = users[u1] - users[u2]
        only_u2 = users[u2] - users[u1]
        print(f" Friends only {u1} has:", only_u1)
        print(f" Friends only {u2} has:", only_u2)
    else:
        print(" One or both users not found.")


#4th def function It combines all the friends from two users and shows the total list without duplicates.
def combine_all_friends():
    u1 = input("Enter first user: ").strip()
    u2 = input("Enter second user: ").strip()
    if u1 in users and u2 in users:
        combined = users[u1] | users[u2]
        print(" Combined friends list:", combined)
    else:
        print(" One or both users not found.")


#5th def function It gives friend suggestions based on the friends of your friends,
# while removing people you already know.
#>> Give me people I don’t know yet but who are friends of my current friends.
def suggest_friends():
    target = input("Get friend suggestions for: ").strip()
    if target not in users:
        print(" User not found.")
        return

    suggestions = set()
    for friend in users[target]:
        if friend in users:
            suggestions |= users[friend]  # Add all their friends

    # Remove current user's existing friends and themselves
    suggestions -= users[target]
    suggestions.discard(target)

    print(" Suggested friends:", suggestions)

def menu():
    while True:
        print("\n Friends List Comparison Tool")
        print("1. Add user and friends")
        print("2. Find mutual friends")
        print("3. Find unique friends")
        print("4. Combine all friends")
        print("5. Get friend suggestions")
        print("6. Exit")

        choice = input("Choose an option from above: ")

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
            print("bye bye!")
            break
        else:
            print(" Invalid choice. Please select 1–6.")

menu() #start the program
