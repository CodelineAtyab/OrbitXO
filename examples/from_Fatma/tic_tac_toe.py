
import random
board = ['1','2','3','4','5','6','7','8','9']
game_running = True

print("Welcome to Tic-Tac-Toe! (You vs Bot)")

# Ask player to choose X or O
player_symbol = input("Do you want to be X or O? ").upper()
while player_symbol not in ['X', 'O']:
    player_symbol = input("Invalid choice. Please choose X or O: ").upper()
bot_symbol = 'O' if player_symbol == 'X' else 'X'
current_player = 'X'  

# Print the board initially
print()
for i in range(0, 9, 3):
    print(f" {board[i]} | {board[i+1]} | {board[i+2]}")
    if i < 6:
        print("---+---+---")
print()

# Start the game loop
while game_running:
    if current_player == player_symbol:
        move = input(f"Your turn ({player_symbol}), choose a cell number (1-9): ")
        if not move.isdigit() or int(move) not in range(1, 10):
            print("Invalid input. Please enter a number between 1 and 9.")
            continue
        move = int(move) - 1
        if board[move] == 'X' or board[move] == 'O':
            print("Cell already taken. Choose another one.")
            continue
    else:

        # Bot's move: choose a random empty cell
        empty_cells = [i for i in range(9) if board[i] != 'X' and board[i] != 'O']
        move = random.choice(empty_cells)
        print(f"Bot ({bot_symbol}) chooses cell {move+1}")
    board[move] = current_player

    # Print the board after the move
    print()
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]}")
        if i < 6:
            print("---+---+---")
    print()

    # Check for winner
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6]              
    ]
    winner = False
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == current_player:
            winner = True
            break
    if winner:
        if current_player == player_symbol:
            print(f"Congratulations! You win!")
        else:
            print("The Bot wins!")
        game_running = False
        continue
    
    # Switch player

    current_player = 'O' if current_player == 'X' else 'X'
