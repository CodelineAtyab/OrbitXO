print("\nWelcome to Text Message Formatter: Character Limit Enforcement!")
print("You should enter any sentance, to count the lenght!")

user_message = input("\nEnter your sentance: ")
print(f"\nLenght of your sentance = {len(user_message)}")

if len(user_message) > 280:
    print("Your message is too long! Let me slice it :) ")
    sliced_message = user_message[:280] + "..."
    print(f"\nYour sliced message = {sliced_message}")
else:
    print("Your message within the range.")
