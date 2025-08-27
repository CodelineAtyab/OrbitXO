import re

email_input = input("Enter and email: ")

valid = re.search("^[\w]+[\w+.-]*@([\w-]+\.)+[\w-]{2,}$", email_input)

if valid:
    print(True)
else:
    print(False)