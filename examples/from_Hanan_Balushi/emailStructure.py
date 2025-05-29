
file = open("examples/from_Hanan_Balushi/emails.txt", "r")

for line in file.readlines():
    email = line.strip()
    if email.count("@") == 1 and len(email[:email.index("@")]) > 1 and "." in email and len(email[email.index("@"):email.rfind(".")]) > 2 and  len(email[email.rfind("."):]) > 2:
        print(f"Email: {email} = Valid Email!")
    else:
        print(f"Email: {email} = Invalid Email!!!")

file.close()
"""CODE EXPLANATION:
the program checks all conditions in one line no. 6:
* len(email[:email.index("@")]) > 1 checks if there are characters before @
* len(email[email.index("@"):email.rfind(".")]) > 2 checks there are characters between @ and the domain dot "."
* len(email[email.rfind("."):]) > 2 checks there are characters after domain dot.
 and rfind() to find the rightmost dot which is the domain dot"""