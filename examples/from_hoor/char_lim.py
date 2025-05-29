SMS = input("ENTER A SENTENCE ")
print(f"\nLenght of your sentance = {len(SMS)}")
if len(SMS) > 280:
    print("SMS is too long , let it be sliced ")
    sliced = SMS[:280] + "..."
    print(f"\nYour sliced message = {sliced}")
else:
    print("Your message within the range.")