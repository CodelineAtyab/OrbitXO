while True:
    print("Frinds List Comparison Tool")
    print("1. Add user and friends")
    print("2. Find mutual friends")
    print("3. Find unique friends")
    print("4. Combine all friends")
    print("5. Get friend suggestions")
    print("6. Exit")


    user_friends_mapping = {}

    a = input("Choose an option: ")
    if a == "1":
            print("Add user and friends \n")
            entName = input("Enter user name: ")
            entFriends = input("Enter friends (comma-separated): ")
            entFriends.split(",")
            print(entFriends)
            user_friends_mapping[entName] = entFriends
            
    elif a == "2":
            print("Find ur mutual friends")
            first_name = input("Enter first user: ")
            secound_name = input("Enter Secound user: ")
            print(first_name)
            print(secound_name)
            mutual_friends = entFriends.intersection()
            print("Mutual friends: ", mutual_friends )
            s = set()
            s.add("")
            

