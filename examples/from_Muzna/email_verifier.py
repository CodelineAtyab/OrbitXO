import sys
def validate_email(email):
    if not email:
        return False
    if email.count("@") != 1:
        return False
    local, domain = email.split("@") #local @ domain 
    if len(local) == 0 or len(domain) == 0:
        return False
    if "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith("."):
            return False
    tld = domain.rsplit(".", 1)[-1]
    if len(tld) < 2:
        return False
    
    return True

email=sys.argv[1]
resalt=validate_email(email)

print (resalt)