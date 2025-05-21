def email_check(email):
    if email == "":
        return False
    if email.count("@") != 1:
        return False

    local, domain = email.split("@")

    if local == "":
        return False
    if domain == "":
        return False
    if "." not in domain:
        return False
    if domain[0] == "." or domain[-1] == ".":
        return False

    last_dot_domain = domain.rfind(".")
    tld = domain[last_dot_domain + 1:]
    if len(tld) < 2:
        return False

    return True
user_email = input("Type your email address: ")
result = email_check(user_email)

if result:
    print("Valid email address!")
else:
    print("Invalid email address!")