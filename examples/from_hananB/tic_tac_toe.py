
import random
 
def checkWinner(board_list, symbol):
    # Check rows
    if board_list[0] == board_list[1] == board_list[2] == symbol: return True
    if board_list[3] == board_list[4] == board_list[5] == symbol: return True
    if board_list[6] == board_list[7] == board_list[8] == symbol: return True
    # Check columns
    if board_list[0] == board_list[3] == board_list[6] == symbol: return True
    if board_list[1] == board_list[4] == board_list[7] == symbol: return True
    if board_list[2] == board_list[5] == board_list[8] == symbol: return True
    # Check diagonals
    if board_list[0] == board_list[4] == board_list[8] == symbol: return True
    if board_list[2] == board_list[4] == board_list[6] == symbol: return True
    return False

def display(board_list):
    print(f"{board_list[0]} | {board_list[1]} | {board_list[2]}")
    print("-----------")
    print(f"{board_list[3]} | {board_list[4]} | {board_list[5]}")
    print("-----------")
    print(f"{board_list[6]} | {board_list[7]} | {board_list[8]}\n")

print("Welcome to Tic Tac Toe!")
user = input("Choose your symbol (X or O): ").upper()
if user == "X":
    bot = "O"
else:
    bot = "X"
print(f"You are {user} the bot is {bot}. Let’s start!\n")

# Now create a list to track
board_list = ['1','2','3','4','5','6','7','8','9']

playing = True
moves = [1,2,3,4,5,6,7,8,9]

display(board_list)

while playing:
    move = input("Your move (choose a number): ")
    while move not in [str(m) for m in moves]:
        move = input("Invalid move. Choose a number: ")

    move = int(move)
    board_list[move-1] = user
    moves.remove(move)

    display(board_list)

    if checkWinner(board_list, user):
        print("Congratulations! You win!")
        break

    if not moves:
        print("It's a draw!")
        break

    botMove = random.choice(moves)
    print(f"Bot chose: {botMove}\n")
    board_list[botMove-1] = bot
    moves.remove(botMove)

    display(board_list)

    if checkWinner(board_list, bot):
        print("You Lose !")
        break

    if not moves:
        print("It's a draw!")
        break







''' import random

def checkWinner(board, symbol):
     # Find the actual character positions
    return (
        (board[0] == symbol and board[4] == symbol and board[8] == symbol) or  # Top row
        (board[24] == symbol and board[28] == symbol and board[32] == symbol) or  # Middle row
        (board[48] == symbol and board[52] == symbol and board[56] == symbol) or  # Bottom row
        (board[0] == symbol and board[24] == symbol and board[48] == symbol) or  # Left column
        (board[4] == symbol and board[28] == symbol and board[52] == symbol) or  # Middle column
        (board[8] == symbol and board[32] == symbol and board[56] == symbol) or  # Right column
        (board[0] == symbol and board[28] == symbol and board[56] == symbol) or  # Diagonal 1
        (board[8] == symbol and board[28] == symbol and board[48] == symbol)     # Diagonal 2
    )


print("Welcome to Tic Tac Toe!")
user = input("Choose your symbol (X or O): ")
if user == "X":
    bot = "O"
else:
    bot = "X"
print("You are "+user+" the bot is "+bot+". Let’s start!\n")
board = "1 | 2 | 3\n-----------\n4 | 5 | 6\n-----------\n7 | 8 | 9\n"
print(board)
playing = True
moves = [1,2,3,4,5,6,7,8,9]

while playing:
    move = str(input("Your move (choose a number): "))
    board = board.replace(move,user)
    print(board)
    winner = checkWinner(board,user)
    if winner:
        print("Congratulations! You win!")
        break
    if len(moves) != 0:
        moves.remove(int(move))
    elif len(moves) == 0:
        playing = False
    if len(moves) != 0:
       botMove = str(random.choice(moves))
    board = board.replace(botMove,bot)
    print("Bot's Move: \n"+board)
    winner = checkWinner(board,bot)
    if winner:
        print("You Lose !")
        break
    if len(moves) != 0:
        moves.remove(int(botMove))
    elif len(moves) == 0:
        playing = False


'''