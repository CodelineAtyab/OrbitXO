import random

print("Welcome to Tic Tac Toe!")

# Player chooses symbol
player = input("Choose X or O: ").upper()
if player == "X":
    bot = "O"
    turn = "player"
else:
    bot = "X"
    turn = "bot"

# Create board
board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

winner = None

while True:
    # Show the board
    print()
    print(board[0], "|", board[1], "|", board[2])
    print("--|---|--")
    print(board[3], "|", board[4], "|", board[5])
    print("--|---|--")
    print(board[6], "|", board[7], "|", board[8])
    print()

    # Player move
    if turn == "player":
        move = input("Choose a spot (1-9): ")
        if move.isdigit():
            move = int(move) - 1
            if move >= 0:
                if move <= 8:
                    if board[move] != "X":
                        if board[move] != "O":
                            board[move] = player
                            turn = "bot"
                        else:
                            print("Spot taken. Try again.")
                            continue
                    else:
                        print("Spot taken. Try again.")
                        continue
                else:
                    print("Number too big. Try 1 to 9.")
                    continue
            else:
                print("Number too small. Try 1 to 9.")
                continue
        else:
            print("Enter a number.")
            continue

    # Bot move
    else:
        empty = []
        i = 0
        while i < 9:
            if board[i] != "X":
                if board[i] != "O":
                    empty.append(i)
            i = i + 1
        bot_move = random.choice(empty)
        board[bot_move] = bot
        print("Bot chose:", bot_move + 1)
        turn = "player"

    # Check win (8 conditions)
    if board[0] == board[1]:
        if board[1] == board[2]:
            winner = turn
    if board[3] == board[4]:
        if board[4] == board[5]:
            winner = turn
    if board[6] == board[7]:
        if board[7] == board[8]:
            winner = turn
    if board[0] == board[3]:
        if board[3] == board[6]:
            winner = turn
    if board[1] == board[4]:
        if board[4] == board[7]:
            winner = turn
    if board[2] == board[5]:
        if board[5] == board[8]:
            winner = turn
    if board[0] == board[4]:
        if board[4] == board[8]:
            winner = turn
    if board[2] == board[4]:
        if board[4] == board[6]:
            winner = turn

    if winner != None:
        break

    # Check draw
    full = True
    j = 0
    while j < 9:
        if board[j] != "X":
            if board[j] != "O":
                full = False
        j = j + 1
    if full:
        break

# Show final board
print()
print(board[0], "|", board[1], "|", board[2])
print("--|---|--")
print(board[3], "|", board[4], "|", board[5])
print("--|---|--")
print(board[6], "|", board[7], "|", board[8])
print()

# Result
if winner == "player":
    print("You win!")
elif winner == "bot":
    print("Hanan wins!")
else:
    print("It's a draw!")