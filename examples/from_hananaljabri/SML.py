print("\nWelcome to the URL checker!")

url_input = input("Enter your URL: ")

if (url_input[:7] == "http://" or url_input[:8] == "https://"):
    if "." in url_input and url_input[-1] != ".":
        print("Valid URL — good job!")
    else:
        print("Invalid URL: missing a dot or ends with a dot.")
else:
    print("Invalid URL: must start with 'http://' or 'https://'.")