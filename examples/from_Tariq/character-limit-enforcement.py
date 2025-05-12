msg = input("write your message: ")
if len(msg) > 280:
    print("your message exceeds the character limit of 280")
    nmsg = msg[0:280] + "..."
    print("your message has been truncated to: ", nmsg)
else:
    print("your message is within the character limit of 280")
    print("your message is: ", msg)