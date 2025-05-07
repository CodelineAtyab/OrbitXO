friends_data = {}
while True:
    # menu:
    print("\n Friends List Comparison Tool")
    print("1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends") 
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")

    choice = int(input("\nChoose an option: "))

 # Add user and friends
    if choice == 1:
        user = input("Enter user name: "). strip()
        friends =input("Enter friends (comma-separated): "). split(',')
        friends_set = set(friend.strip() for friend in friends)
        friends_data[user] = friends_set

# Find mutual friends
    elif choice == 2:
        user1 = input("Enter first user: ")
        user2 = input("Enter second user: ")
        
        if user1 in friends_data and user2 in friends_data:
            friend1 =friends_data[user1]
            friend2 =friends_data[user2]

            mutual = friend1 & friend2
            print("Mutual friends: ", mutual)
        

# Find unique friends
    elif choice == 3:
        user1 = input("Enter first user: ")
        user2 = input("Enter second user: ")

        if user1 in friends_data and user2 in friends_data:
            friend1 =friends_data[user1]
            friend2 =friends_data[user2]

            unique1 = friend1 - friend2
            unique2 = friend2 - friend1

            print(f"Friends only {user1} has: ", unique1)
            print(f"Friends only {user2} has: ", unique2)


# Combine all friends
    elif choice == 4:
        user1 = input("Enter first user: ")
        user2 = input("Enter second user: ")
        
        if user1 in friends_data and user2 in friends_data:
            friend1 =friends_data[user1]
            friend2 =friends_data[user2]

            union = friend1 | friend2
            print("All friends: ", union)


# Get friend suggestions
    elif choice == 5:
        f1 = input("Get friend suggestions for: "). strip()
        if f1 not in friends_data:
            print (" friend not found")
          
        f1_friend = friends_data[f1]
        sugg = set()
        for friend in f1_friend:
            if friend in friends_data:
            
                sugg |= friends_data[friend]
        sugg -= f1_friend
        sugg.discard(f1)
        print("Suggested friends: ", sugg)


# Exit
    elif choice == 6:
       print(" Thank you!")
       break


    else:
       print("invalid input")
