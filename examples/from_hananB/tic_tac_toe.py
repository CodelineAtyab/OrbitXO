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
