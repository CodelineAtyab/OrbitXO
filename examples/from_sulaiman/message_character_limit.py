user_message = input("Enter your message: ")
if len(user_message) > 280:
    print(user_message[0:280] + "...")
else:
    print(user_message)