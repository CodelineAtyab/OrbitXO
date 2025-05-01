# Create the board
board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

current_player = "X"  # Human
game_over = False

while game_over == False:
    # Print the board
    r = 0
    while r < 3:
        print(board[r][0] + " | " + board[r][1] + " | " + board[r][2])
        print("---------")
        r = r + 1

    if current_player == "X":
        print("Your turn (X)")
        valid = False
        while valid == False:
            row_input = input("Enter row (0, 1, or 2): ")
            col_input = input("Enter column (0, 1, or 2): ")
            if row_input.isdigit() and col_input.isdigit():
                row = int(row_input)
                col = int(col_input)
                if row >= 0 and row <= 2 and col >= 0 and col <= 2:
                    if board[row][col] == " ":
                        valid = True
                    else:
                        print("Cell already taken.")
                else:
                    print("Choose numbers between 0 and 2.")
            else:
                print("Please enter numbers only.")
    else:
        print("Bot's turn (O)")
        row = 0
        col = 0
        found = False
        while found == False:
            if board[row][col] == " ":
                found = True
            else:
                col = col + 1
                if col > 2:
                    col = 0
                    row = row + 1

    board[row][col] = current_player

    # Check win
    win = False
    if board[0][0] == current_player and board[0][1] == current_player and board[0][2] == current_player:
        win = True
    elif board[1][0] == current_player and board[1][1] == current_player and board[1][2] == current_player:
        win = True
    elif board[2][0] == current_player and board[2][1] == current_player and board[2][2] == current_player:
        win = True
    elif board[0][0] == current_player and board[1][0] == current_player and board[2][0] == current_player:
        win = True
    elif board[0][1] == current_player and board[1][1] == current_player and board[2][1] == current_player:
        win = True
    elif board[0][2] == current_player and board[1][2] == current_player and board[2][2] == current_player:
        win = True
    elif board[0][0] == current_player and board[1][1] == current_player and board[2][2] == current_player:
        win = True
    elif board[0][2] == current_player and board[1][1] == current_player and board[2][0] == current_player:
        win = True

    if win == True:
        r = 0
        while r < 3:
            print(board[r][0] + " | " + board[r][1] + " | " + board[r][2])
            print("---------")
            r = r + 1
        if current_player == "X":
            print("You win!")
        else:
            print("Bot wins!")
        game_over = True
    else:
        # Check for draw
        full = True
        i = 0
        while i < 3:
            j = 0
            while j < 3:
                if board[i][j] == " ":
                    full = False
                j = j + 1
            i = i + 1

        if full == True:
            r = 0
            while r < 3:
                print(board[r][0] + " | " + board[r][1] + " | " + board[r][2])
                print("---------")
                r = r + 1
            print("It's a draw!")
            game_over = True
        else:
            # Switch turn
            if current_player == "X":
                current_player = "O"
            else:
                current_player = "X"