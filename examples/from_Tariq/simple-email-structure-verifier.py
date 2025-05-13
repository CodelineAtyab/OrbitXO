email = input("Enter the email address: ")
if "@" in email and "." in email and\
    email.index("@")< email.index(".") and\
    email.index("@") > 0 and\
    email.index(".") < len(email) - 1 and\
    email.index(".") - email.index("@") > 1 and\
    email.count("@") == 1 and\
    len(email[email.rindex(".")+1:]) > 2 :
    print("Valid email address")
else:
    print("Invalid email address")
    