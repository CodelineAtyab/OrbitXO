import re

file = open("examples/from_Hanan_Balushi/urls.txt", "r")
for line in file.readlines():
    url = line.strip()
    if url.startswith("http://") or url.startswith("https://"): #check if begining is correct
        if "." in url and not url.endswith(".") and len(url[url.index("."):])>2: # check if here is domain after .
            print(f"URL: {url} = Valid URL!")
        else:
            print(f"URL: {url} = Invalid URL!!!") #if beginning is correct but there is no domain print invalid
    else:
        print(f"URL: {url} = Invalid URL!!!")
file.close()

