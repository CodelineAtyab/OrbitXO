import random

print("Welcome to Tic Tac Toe!\nChoose your symbol (X or O): X\nYou are X, the bot is O. Let’s start!\n")
positions = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

turns = 0
your_turn = True
winner_found = False


while turns < 9 and not winner_found:
    for i in range(len(positions)):
        print(positions[i][0] + " | " + positions[i][1] + " | " + positions[i][2])
        print("-----------")
    print()

    if your_turn:
        your_move = input("Your move (choose a number position): ")

        invalid_move = ((your_move not in positions[0]) and (your_move not in positions[1]) and (your_move not in positions[2])) or (your_move in ["X", "O"])

        while invalid_move:
            your_move = input("that is not a valid or available position, do it again: ")
            invalid_move = ((your_move not in positions[0]) and (your_move not in positions[1]) and (your_move not in positions[2])) or (your_move in ["X", "O"])
        for row in range(len(positions)):
            for col in range(len(positions)):
                if positions[row][col] == your_move:
                    positions[row][col] = "X"
        your_turn = False
    else:
        print("Bot's move:")
        bot_pos = random.randrange(1,10)
        invalid_move = (str(bot_pos) not in positions[0]) and (str(bot_pos) not in positions[1]) and (str(bot_pos) not in positions[2])
        while invalid_move:
            bot_pos = random.randrange(1,10)
            invalid_move =(str(bot_pos) not in positions[0]) and (str(bot_pos) not in positions[1]) and (str(bot_pos) not in positions[2])
        for row in range(len(positions)):
            for col in range(len(positions)):
                if positions[row][col] == str(bot_pos):
                    positions[row][col] = "O"
        print(positions)
        your_turn = True

    for index in range(3):
        if positions[index][0] == positions[index][1] == positions[index][2]:
            winner_found = True
            print("Game ended")
            if positions[index][0] == "X":
                print("X wins")
            else:
                print("O wins")
        if positions[0][index] == positions[1][index] == positions[2][index]:
            winner_found = True
            if positions[0][index] == "X":
                print("X wins")
            else:
                print("O wins")
    if positions[0][0] == positions[1][1] == positions[2][2]:
        winner_found = True
        if positions[0][0] == "X":
            print("X wins")
        else:
            print("O wins")
    if positions[0][2] == positions[1][1] == positions[2][0]:
        winner_found = True
        if positions[0][0] == "X":
            print("X wins")
        else:
            print("O wins")

if winner_found == False:
    print("We have a Draw")