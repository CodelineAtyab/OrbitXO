
users = {}

print("Welcome to the Friends List Comparison Tool!")

running = True
while running:
    print("Menu:")
    print("1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")
    
    choice = input("Choose an option: ")

    if choice == "1":
        name = input("Enter user name: ")
        friends_input = input("Enter friends (comma-separated): ")
        friend_names = friends_input.split(",")
        friend_set = set()
        
        for f in friend_names:
            if f != "":
                friend_set.add(f)
        
        users[name] = friend_set
        print(name + "'s friends have been added.\n")

    elif choice == "2":
        user1 = input("Enter first user: ")
        user2 = input("Enter second user: ")

        if user1 in users and user2 in users:
            mutual = users[user1] & users[user2]
            print("Mutual friends: ", mutual, "\n")
        else:
            print("One or both users not found.\n")

    elif choice == "3":
        user1 = input("Enter first user: ")
        user2 = input("Enter second user: ")

        if user1 in users and user2 in users:
            only1 = users[user1] - users[user2]
            only2 = users[user2] - users[user1]
            print("Friends only " + user1 + " has: ", only1)
            print("Friends only " + user2 + " has: ", only2)
            print("")
        else:
            print("One or both users not found.\n")

    elif choice == "4":
        user1 = input("Enter first user: ")
        user2 = input("Enter second user: ")

        if user1 in users and user2 in users:
            combined = users[user1] | users[user2]
            print("All friends from both users: ", combined, "\n")
        else:
            print("One or both users not found.\n")

    elif choice == "5":

        user = input("Get friend suggestions form: ")
        if user not in users:  
            print("User not found.\n")
        else:
            suggestions = set()    
            for friend in users[user]:
                if friend in users:
                    for f in users[friend]:
                        if f != user and f not in users[user]:
                            suggestions.add(f) 
            print(f"Suggested friends: {suggestions}\n")

    elif choice == "6":
        print("Goodbye!")
        running = False
    else:
        print("Invalid option. Try again.\n") 