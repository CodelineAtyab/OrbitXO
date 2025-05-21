import re

file = open("examples/from_Hanan_Balushi/emails.txt", "r")
for line in file.readlines():
    email = line.strip()
    if re.search(r"^[a-zA-Z0-9_+-.]{2,}@[a-zA-Z]{2,}\.[a-zA-Z]{2,}", email):
        print(f"Email: {email} = Valid Email!")
    else:
        print(f"Email: {email} = Invalid Email!!!") #if beginning is correct but there is no domain print invalid
file.close()
