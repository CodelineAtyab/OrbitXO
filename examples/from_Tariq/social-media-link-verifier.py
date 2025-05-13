msg = input("write valid URL: ")
if msg.startswith("https://") or msg.startswith("http://") and "." in msg[8:]:
    domaindot = msg.find(".")
    if domaindot > 0 and domaindot < len(msg) - 1:
         print("Valid URL")
    else:
        print("Invalid URL")
else:
    print("Invalid URL")