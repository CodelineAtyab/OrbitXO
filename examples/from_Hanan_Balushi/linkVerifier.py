import re

file = open("examples/from_Hanan_Balushi/urls.txt", "r")
for line in file.readlines():
    url = line.strip()
    if url.startswith("http://") or url.startswith("https://"):
        if re.search(r"\.[a-zA-Z]+", url):
            print(f"URL: {url} = Valid URL!")
    else:
        print(f"URL: {url} = Invalid URL!!!")
file.close()

