user_email = input("Enter your email: ")

if "@" in user_email and "." in user_email and\
   user_email.count("@") == 1 and\
   user_email.index("@") > 0 and\
   user_email.index("@") < len(user_email)-1 and\
   user_email[user_email.index("@")+1] != "." and\
   user_email.rindex(".") > user_email.index("@") and\
   len(user_email[user_email.rindex(".")+1:]) >= 2:
    print("True")
else:
    print("False")