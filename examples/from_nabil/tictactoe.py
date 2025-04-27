import random

# Display the board
def print_board(b):
    print()
    print(f" {b[0]} | {b[1]} | {b[2]}")
    print("---+---+---")
    print(f" {b[3]} | {b[4]} | {b[5]}")
    print("---+---+---")
    print(f" {b[6]} | {b[7]} | {b[8]}")
    print()

# Check for a win
def check_winner(b, s):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    return any(b[x]==b[y]==b[z]==s for x,y,z in wins)

# Get player move
def player_move(board):
    while True:
        move = input("Your move (1-9): ")
        if move.isdigit() and 1 <= int(move) <= 9:
            idx = int(move) - 1
            if board[idx] not in ['X','O']:
                return idx
        print("Invalid move, try again.")

# Get bot move
def bot_move(board):
    empty = [i for i in range(9) if board[i] not in ['X','O']]
    return random.choice(empty)

# Main game
def main():
    print("Welcome to Tic Tac Toe!")
    player = ''
    while player not in ['X', 'O']:
        player = input("Choose your symbol (X or O): ").upper()

    bot = 'O' if player == 'X' else 'X'
    print(f"You are {player}, bot is {bot}. Let's play!")

    board = [str(i+1) for i in range(9)]
    print_board(board)

    turn = 'player' if player == 'X' else 'bot'

    for _ in range(9):
        if turn == 'player':
            idx = player_move(board)
            board[idx] = player
            print_board(board)
            if check_winner(board, player):
                print("You win!")
                return
            turn = 'bot'
        else:
            print("Bot's move:")
            idx = bot_move(board)
            board[idx] = bot
            print_board(board)
            if check_winner(board, bot):
                print("Bot wins!")
                return
            turn = 'player'
    print("It's a draw!")

if __name__ == "__main__":
    main()