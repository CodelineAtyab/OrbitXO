
friends = {}  #set

while True:
    print("Friends List Comparison Tool")
    print("1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit\n")

    option = input("Choose an option: ")


#option 1
    if option == '1':
        name_input = input("Enter user name: ")
        friends_input = input("Enter friends name (separate the names with comma): ")

        friend_names = friends_input.split(",")   #to split the list using , 
        friend_set = set()    #to create a set to store the friends name 
        for name in friend_names:
            name = name.strip()
            if name != "":  #to check that the name is not empty
                friend_set.add(name)

        friends[name_input] = friend_set  # store the names in friends set
        print(f"{name_input}'s friends list updated.\n")


#option 2
    elif option == '2':
        f1 = input("Enter first name: ")
        f2 = input("Enter second name: ")

        if f1 in friends and f2 in friends:  #check both f1 and f2 exist 
            mutual = friends[f1] & friends[f2]
            print(f"Mutual friends: {mutual}\n")
        else:
            print("One or both users not found.\n")


#option 3 
    elif option == '3':
        f1 = input("Enter first name: ")
        f2 = input("Enter second name: ")

        if f1 in friends and f2 in friends:
            only_user1 = friends[f1] - friends[f2]  #for the friends only f1 has
            only_user2 = friends[f2] - friends[f1]     #for the friends only f2 has
            print(f"Friends only {f1} has: {only_user1}")   #display f1 unique friends
            print(f"Friends only {f2} has: {only_user2}\n")   #display f2 unique friends
        else:
            print("One or both users not found.\n")  #if the friend not found 



    elif option == '4':
        f1 = input("Enter first user: ")
        f2 = input("Enter second user: ")

        if f1 in friends and f2 in friends:
            comb = friends[f1] | friends[f2]   #To set union (Smae friends)
            print(f"All friends from both users: {comb}\n")
        else:
            print("One or both users not found.\n")



    elif option == '5':
        user = input("Get friend suggestions form: ")

        if user not in friends:  #to check if the user exist
            print("User not found.\n") 
        else:
            suggestions = set()    #empty set to store the suggestion
            for friend in friends[user]:
                if friend in friends:
                    for f in friends[friend]:
                        if f != user and f not in friends[user]:
                            suggestions.add(f) #to add if not user and not in the same friend set
            print(f"Suggested friends: {suggestions}\n")



    elif option == '6':
        print("Exiting the tool.")
        break

    else:
        print("Invalid choice. Please try again.\n")  #for the options other than 1-6
