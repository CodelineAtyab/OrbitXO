email_input = input("Input the email: ")
if email_input.count("@") == 1 and \
not email_input.startswith("@") and \
not email_input.endswith("@"):
    local = email_input[:email_input.find("@")]
    domain = email_input[email_input.find("@")+1:]
    if "." in domain and \
    not domain.startswith(".") and \
    not domain.endswith(".") and \
    len(domain[domain.rfind(".")+1:]) > 1:
        print(True)
    else:
        print(False)
else:
    print(False)