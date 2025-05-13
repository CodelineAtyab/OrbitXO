url = input("Enter a URL")
if url.startswith("https://") or url.startswith("http://") and "." in url:
    print(True)
else:
    print(False)