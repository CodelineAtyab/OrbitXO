# Initialize board (1-9)
board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
# Asking the player to choose X or O
player = ""
bot = ""
while player != "X" and player != "O":
    player = input("Choose X or O: ").upper()
if player == "X":
    bot = "O"
else:
    bot = "X"
# Show the board
print()
print(" " + board[0] + " | " + board[1] + " | " + board[2])
print("---+---+---")
print(" " + board[3] + " | " + board[4] + " | " + board[5])
print("---+---+---")
print(" " + board[6] + " | " + board[7] + " | " + board[8])
print()
# Start the game
game_over = False
turn = "player"
while game_over == False:
    if turn == "player":
        move = input("Choose a position (1-9): ")
        if move == "1" or move == "2" or move == "3" or move == "4" or move == "5" or move == "6" or move == "7" or move == "8" or move == "9":
            move = int(move) - 1
            if board[move] != "X" and board[move] != "O":
                board[move] = player
                turn = "bot"
            else:
                print("That spot is already taken.")
        else:
            print("Invalid input. Type a number between 1 and 9.")
    else:
        print("It is bot turn...")
        bot_move_done = False
        i = 0
        while bot_move_done == False and i < 9:
            if board[i] != "X" and board[i] != "O":
                board[i] = bot
                bot_move_done = True
                turn = "player"
            i = i + 1
    # Show the board after each move
    print()
    print(" " + board[0] + " | " + board[1] + " | " + board[2])
    print("---+---+---")
    print(" " + board[3] + " | " + board[4] + " | " + board[5])
    print("---+---+---")
    print(" " + board[6] + " | " + board[7] + " | " + board[8])
    print()
    # Check for a win
    if (board[0] == board[1] == board[2] and (board[0] == "X" or board[0] == "O")) or \
       (board[3] == board[4] == board[5] and (board[3] == "X" or board[3] == "O")) or \
       (board[6] == board[7] == board[8] and (board[6] == "X" or board[6] == "O")) or \
       (board[0] == board[3] == board[6] and (board[0] == "X" or board[0] == "O")) or \
       (board[1] == board[4] == board[7] and (board[1] == "X" or board[1] == "O")) or \
       (board[2] == board[5] == board[8] and (board[2] == "X" or board[2] == "O")) or \
       (board[0] == board[4] == board[8] and (board[0] == "X" or board[0] == "O")) or \
       (board[2] == board[4] == board[6] and (board[2] == "X" or board[2] == "O")):
        game_over = True
        if turn == "bot":
            print("You win! CONGRATULATIONS!")
        else:
            print("OPS! Bot wins!")
    # Check for draw
    empty_spaces = 0
    for j in range(9):
        if board[j] != "X" and board[j] != "O":
            empty_spaces = empty_spaces + 1
    if empty_spaces == 0 and game_over == False:
        print("It's a draw!")
        game_over = True