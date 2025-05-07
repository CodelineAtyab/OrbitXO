
friendships = {}

print("Friends List Comparison Tool\n1. Add user and friends\n2. Find mutual friends\n3. Find unique friends\n4. Combine all friends\n5. Get friend suggestions\n6. Exit\n")

option = input("choose an option: ")

while option != "6":
    if option == "1":
        name = input("\nEnter user name: ")
        freinds_name = input("Enter friends (comma-separated): ")

        if name not in friendships:
            friendships[name] = set()
        
        for friend in freinds_name.split(","):
            friendships[name].add(friend.strip())
    
    if option == "2":
        user1 = input("Enter first user: ")
        user2 = input("Enter second user: ")
        mutual = friendships[user1].intersection(friendships[user2])
        print(f"Mutual friends: {mutual}")

    if option == "3":
        user1 = input("Enter first user: ")
        user2 = input("Enter second user: ")
        onlyUser1 = friendships[user1].difference(friendships[user2])
        onlyUser2 = friendships[user2].difference(friendships[user1])
        print(f"Friends only {user1} has: {onlyUser1}")
        print(f"Friends only {user2} has: {onlyUser2}")

    if option == "4":
        user1 = input("Enter first user: ")
        user2 = input("Enter second user: ")
        both = friendships[user1].union(friendships[user2])
        print(f"{user1} and {user2} friends combined: {both}")

    if option == "5":
        fName = input("Get friend suggestions for: ")
        suggests = set()
        for friend in friendships: #loop over the friends in the dict
            if friendships[friend].intersection(friendships[fName]): #if there is mutual friends then find friend of friends
                suggests.update(friendships[friend] - friendships[friend].intersection(friendships[fName])) #update the suggestion set with friends of friends
        print(f"Suggested friends: {suggests}")

        

    option = input("\nchoose an option: ")
    