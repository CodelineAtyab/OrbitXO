import random

print("Welcome to Tic Tac Toe!")
user_choice = input("Choose your symbol (X OR O): ").upper()


bot_choice = 'O' if user_choice == 'X' else 'X'
print(f"You are {user_choice}, the bot is {bot_choice}. Let's start!")


board = [' ' for _ in range(9)]

def display_board(board):
    print()
    print(f" {board[0]} | {board[1]} | {board[2]}")
    print("----+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("----+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}")
    print()


def player_move(board, user_choice):
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            if move < 0 or move > 8:
                print("Invalid position! Choose a number between 1 and 9.")
            elif board[move] != ' ':
                print("Position already taken! Choose another one.")
            else:
                board[move] = user_choice
                break
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 9.")


def bot_move(board, bot_choice):
    available_moves = [i for i, spot in enumerate(board) if spot == ' ']
    move = random.choice(available_moves)
    board[move] = bot_choice
    print(f"Bot placed {bot_choice} in position {move + 1}")


def check_winner(board, symbol):
  
    if (board[0] == symbol and board[1] == symbol and board[2] == symbol) or \
       (board[3] == symbol and board[4] == symbol and board[5] == symbol) or \
       (board[6] == symbol and board[7] == symbol and board[8] == symbol):
        return True

  
    if (board[0] == symbol and board[3] == symbol and board[6] == symbol) or \
       (board[1] == symbol and board[4] == symbol and board[7] == symbol) or \
       (board[2] == symbol and board[5] == symbol and board[8] == symbol):
        return True

  
    if (board[0] == symbol and board[4] == symbol and board[8] == symbol) or \
       (board[2] == symbol and board[4] == symbol and board[6] == symbol):
        return True

    return False


def is_draw(board):
    return ' ' not in board


while True:
    display_board(board)
    player_move(board, user_choice)
    
    if check_winner(board, user_choice):
        display_board(board)
        print("Congratulations! You win!")
        break

    if is_draw(board):
        display_board(board)
        print("It's a draw!")
        break

    bot_move(board, bot_choice)

    if check_winner(board, bot_choice):
        display_board(board)
        print("Bot wins! Better luck next time.")
        break

    if is_draw(board):
        display_board(board)
        print("It's a draw!")
        break
