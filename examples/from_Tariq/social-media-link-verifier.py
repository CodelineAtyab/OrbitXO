msg = input("write valid URL: ")
if msg.startswith("https://"): 
    x=8
elif msg.startswith("http://"):
    x=7 
if (msg.startswith("https://") or msg.startswith("http://")) and "." in msg[x:]:
    domaindot = msg.find(".")
    if domaindot > 0 and domaindot < len(msg) - 1:
         print("Valid URL")
    else:
        print("Invalid URL")
else:
    print("Invalid URL")
