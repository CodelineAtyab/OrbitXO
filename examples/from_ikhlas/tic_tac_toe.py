
print("Welcome to Tic Tac Toe!")

board = ["1","2","3","4","5","6","7","8","9"]


player = input("Choose your symbol (X or O): ")

if player == "X":
    bot = "O"
else:
    bot = "X"

print("You are",player+ ",the bot is", bot+" .Let’s start!")

# To print the board 
def print_board():
    print()
    print(" ", board[0], "|", board[1], "|", board[2])
    print(" -----------")
    print(" ", board[3], "|", board[4], "|", board[5])
    print(" -----------")
    print(" ", board[6], "|", board[7], "|", board[8])
    print()

#game start
winner = None
turn = "Player"

# Player turn
for move in range(9):
    print_board()


    if turn == "Player":
        print("Your move (choose a number):")
        position = input()
        if position in board:
            index = board.index(position) #To find where the player input on the board
            board[index] = player
            turn = "bot"
        else:
            print("Invalid move. Try again.")
            continue

    else:
        #bot turn
        print("Bot's move: ")
        placed = False    
        for i in range(9):
            if board[i] != "X" and board[i] != "O" and not placed:  #Check the place with no X , O mark
                board[i] = bot
                placed = True
        turn = "Player"

   

    #Rows
    if board[0] == board[1] == board[2]: winner = board[0]
    if board[3] == board[4] == board[5]: winner = board[3]
    if board[6] == board[7] == board[8]: winner = board[6]

    #Columns
    if board[0] == board[3] == board[6]: winner = board[0]
    if board[1] == board[4] == board[7]: winner = board[1]
    if board[2] == board[5] == board[8]: winner = board[2]

    #Diagonals
    if board[0] == board[4] == board[8]: winner = board[0]
    if board[2] == board[4] == board[6]: winner = board[2]

    if winner != None:  #check if the winner variable set
        print_board()
        if winner == player:  #check the winner X
            print("Congratulations! You win!")
        else:
            print("Bot wins! Better luck next time.")
        break

# In case of no winner
if winner == None:
    print_board()
    print("It's a draw!")
