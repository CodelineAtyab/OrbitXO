friend_network = {}
while True:
    print("show the menue of program:")
    print("1. Add a person and their friends")
    print("2. Show mutual friends between two people")
    print("3. Show unique friends for each person")
    print("4. Show all combined friends")
    print("5. Suggest friends")
    print("6. Exit")

    choice = input("choice a number between 1 to 6: ")

    if choice == "1":
        name = input("Enter the person name: ")

        friends = []
        print("Now enter their friends.")
        while True:
            friend_name = input("Friend name: ")
            friends.append(friend_name)
            friend_network[name] = friends
            print(f"{name} has been added with {len(friends)} friend: {friends}")

    elif choice == "2":
        name1 = input("First person name: ")
        name2 = input("Second person name: ")

        if name1 not in friend_network or name2 not in friend_network:
            print("One or both people are not in the system.")
        else:
            mutual = []
            for friend in friend_network[name1]:
                if friend in friend_network[name2]:
                    mutual.append(friend)
            
            if mutual:
                print(f"Mutual friends of {name1} and {name2}: {mutual}")
            else:
                print(f"No mutual friends between {name1} and {name2}.")

    elif choice == "3":
        name1 = input("First person's name: ")
        name2 = input("Second person's name: ")

        if name1 not in friend_network or name2 not in friend_network:
            print("One or both people are not in the system.")
        else:
            unique1 = []
            for friend in friend_network[name1]:
                if friend not in friend_network[name2]:
                    unique1.append(friend)
                    
            unique2 = []
            for friend in friend_network[name2]:
                if friend not in friend_network[name1]:
                    unique2.append(friend)
            
            print(f"Friends only {name1} has: {unique1}")
            print(f"Friends only {name2} has: {unique2}")

    elif choice == "4":
        name1 = input("First person's name: ")
        name2 = input("Second person's name: ")

        if name1 not in friend_network or name2 not in friend_network:
            print("One or both people are not in the system.")
        else:
            combined = []
            for friend in friend_network[name1]:
                if friend not in combined:
                    combined.append(friend)
            
            for friend in friend_network[name2]:
                if friend not in combined:
                    combined.append(friend)
                    
            print(f"All friends combined for {name1} and {name2}: {combined}")

    elif choice == "5":
        name = input("Whose friend suggestions do you want? ")

        if name not in friend_network:
            print("This person is not in our system.")
        else:
            suggestions = []
            for friend in friend_network[name]:
                if friend in friend_network:
                    for fof in friend_network[friend]:
                        if fof != name and fof not in friend_network[name] and fof not in suggestions:
                            suggestions.append(fof)
            if suggestions:
                print(f"Suggestions for {name}: {suggestions}")
            else:
                print(f"No new suggestions for {name} right now.")

    elif choice == "6":
        print("Thanks for using the Friends List Manager. Goodbye!")
        break

    else:
        print("Invalid option. Please enter a number from 1 to 6.")