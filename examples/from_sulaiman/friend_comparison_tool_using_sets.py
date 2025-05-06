friend_comparison = {}
friend_comparison_tool_operation = True

while friend_comparison_tool_operation:

    print("Friends List Comparison Tool:\n"
    "1. Add user and friends\n"
    "2. Find mutual friends\n"
    "3. Find unique friends\n"
    "4. Combine all friends\n"
    "5. Get friend suggestions\n"
    "6. Exit\n")

    option = int(input("Choose an option: "))

    if option == 1:
        friend_user = input("Enter user name: ").lower().strip()
        friend_group = input("Enter friends (comma-separated): ").lower().strip()

        friend_set = set(friend_group.replace(" ", "").split(","))
        friend_comparison[friend_user] = friend_set
    elif option == 6:
        friend_comparison_tool_operation = False
        print("Exiting program, thank you for using the comparison tool")
    elif not friend_comparison:
        print("\nfriend lists are empty\n")
    elif option == 2:
        first_user = input("Enter first user: ").lower().strip()
        second_user = input("Enter second user: ").lower().strip()

        mutual_friend = friend_comparison[first_user] & friend_comparison[second_user]
        print(mutual_friend)
    elif option == 3:
        first_user = input("Enter first user: ").lower().strip()
        second_user = input("Enter second user: ").lower().strip()

        first_user_unique_friends = friend_comparison[first_user] - friend_comparison[second_user]
        first_user_unique_friends.discard(second_user)
        second_user_unique_friends = friend_comparison[second_user] - friend_comparison[first_user]
        second_user_unique_friends.discard(first_user)
        print(first_user + "'s unique friends are: " + str(first_user_unique_friends))
        print(second_user + "'s unique friends are: " + str(second_user_unique_friends))
    elif option == 4:
        friend_combine = set()
        for user in friend_comparison:
            friend_combine = friend_combine.union(friend_comparison[user])
        print(friend_combine)
    elif option == 5:
        friend_user = input("Enter user name: ").lower().strip()
        friend_suggestion = set()
        for user in friend_comparison:
            friend_suggestion = friend_suggestion.union(friend_comparison[user] - friend_comparison[friend_user])
            friend_suggestion.discard(friend_user)
        print(friend_suggestion)