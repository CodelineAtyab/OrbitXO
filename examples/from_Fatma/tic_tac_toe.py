
# Initial board with numbers 1 to 9
board = ['1','2','3','4','5','6','7','8','9']
# Welcome and symbol selection
print("Welcome to Tic Tac Toe!")

player = input("Choose X or O: ").upper()
if player == "X":
    bot = "O"
else:
    player = "O"
    bot = "X"
turn = "Player"
game_over = False
# Start the game loop
while not game_over:
    # Display the board
    print()
    print(" " + board[0] + " | " + board[1] + " | " + board[2])
    print("---+---+---")
    print(" " + board[3] + " | " + board[4] + " | " + board[5])
    print("---+---+---")
    print(" " + board[6] + " | " + board[7] + " | " + board[8])
    print()
    
    if turn == "Player":
        try:
            pos = int(input("Enter position (1-9): ")) - 1
            if board[pos] not in ["X", "O"]:
                board[pos] = player
                # Check if player wins
                if (board[0] == board[1] == board[2] == player or
                    board[3] == board[4] == board[5] == player or
                    board[6] == board[7] == board[8] == player or
                    board[0] == board[3] == board[6] == player or
                    board[1] == board[4] == board[7] == player or
                    board[2] == board[5] == board[8] == player or
                    board[0] == board[4] == board[8] == player or
                    board[2] == board[4] == board[6] == player):
                    print()
                    print(" " + board[0] + " | " + board[1] + " | " + board[2])
                    print("---+---+---")
                    print(" " + board[3] + " | " + board[4] + " | " + board[5])
                    print("---+---+---")
                    print(" " + board[6] + " | " + board[7] + " | " + board[8])
                    print()
                    print("You win!")
                    game_over = True
                else:
                    turn = "Bot"
            else:
                print("That spot is taken. Try again.")
        except:
            print("Invalid input. Try a number from 1 to 9.")
    else:
        print("Bot is playing...")
        for i in range(9):
            if board[i] not in ["X", "O"]:
                board[i] = bot
                break
        # Check if bot wins
        if (board[0] == board[1] == board[2] == bot or
            board[3] == board[4] == board[5] == bot or
            board[6] == board[7] == board[8] == bot or
            board[0] == board[3] == board[6] == bot or
            board[1] == board[4] == board[7] == bot or
            board[2] == board[5] == board[8] == bot or
            board[0] == board[4] == board[8] == bot or
            board[2] == board[4] == board[6] == bot):
            print()
            print(" " + board[0] + " | " + board[1] + " | " + board[2])
            print("---+---+---")
            print(" " + board[3] + " | " + board[4] + " | " + board[5])
            print("---+---+---")
            print(" " + board[6] + " | " + board[7] + " | " + board[8])
            print()
            print("Bot wins!")
            game_over = True
        else:
            turn = "Player"
    # Check for draw
    if " " not in board:
        print("It's a draw!")
        break