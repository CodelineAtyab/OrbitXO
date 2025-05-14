import sys


url=input("Enter URL :  ")

def url_verifiecation(url):

    if not url:
        return False

    if url.startswith("http://"):
        remainder = url[7:] 
        if '.' in remainder:
            return True
        else:
            return False
    elif url.startswith("https://"):
        remainder = url[8:] 
        if '.' in remainder:
            return True
        else:
            return False
    else:
        return False
    

print(url_verifiecation(url))

