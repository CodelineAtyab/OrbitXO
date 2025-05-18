print("\nWelcome to URL task :)")

user_url = input("Please type your link here: ")

if (user_url.startswith("http://") or user_url.startswith("https://")):
    if "." in user_url and not user_url.endswith("."):
        print("True URL .. well done :) ")
    else:
        print("Invalid URL (no dot found)")
else:
    print("Invalid URL (must start with http:// or https://)")
