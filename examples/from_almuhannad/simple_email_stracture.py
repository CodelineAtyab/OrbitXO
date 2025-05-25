user_email = input("Enter your email: ")

if "@" in user_email and "." in user_email and\
   user_email.index("@") > 0 and\
   user_email.index("@") < len(user_email)-1 and\
   user_email.index(".") > user_email.index("@") and\
   len(user_email[user_email.rindex(".")+1]) > 2:
    print("Email valid")
else:
    print("Email in unvalid")


