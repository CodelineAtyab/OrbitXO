user_inp = input("Enter a message: ")

if len(user_inp) > 280:
    user_sliced = user_inp[:277] + "..."
    print("------------------------------------- \n")
    print(user_sliced)
else:
    print(user_inp)