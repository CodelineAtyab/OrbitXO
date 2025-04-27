from tabulate import tabulate
import time
import random

def check_winner(board):
    if board[0][0] == 'X' and board[0][1] == 'X' and board[0][2] == 'X':
        return 'X'
    if board[0][0] == 'O' and board[0][1] == 'O' and board[0][2] == 'O':
        return 'O'
    if board[1][0] == 'X' and board[1][1] == 'X' and board[1][2] == 'X':
        return 'X'
    if board[1][0] == 'O' and board[1][1] == 'O' and board[1][2] == 'O':
        return 'O'
    if board[2][0] == 'X' and board[2][1] == 'X' and board[2][2] == 'X':
        return 'X'
    if board[2][0] == 'O' and board[2][1] == 'O' and board[2][2] == 'O':
        return 'O'
    if board[0][0] == 'X' and board[1][0] == 'X' and board[2][0] == 'X':
        return 'X'
    if board[0][0] == 'O' and board[1][0] == 'O' and board[2][0] == 'O':
        return 'O'
    if board[0][1] == 'X' and board[1][1] == 'X' and board[2][1] == 'X':
        return 'X'
    if board[0][1] == 'O' and board[1][1] == 'O' and board[2][1] == 'O':
        return 'O'
    if board[0][2] == 'X' and board[1][2] == 'X' and board[2][2] == 'X':
        return 'X'
    if board[0][2] == 'O' and board[1][2] == 'O' and board[2][2] == 'O':
        return 'O'
    if board[0][0] == 'X' and board[1][1] == 'X' and board[2][2] == 'X':
        return 'X'
    if board[0][0] == 'O' and board[1][1] == 'O' and board[2][2] == 'O':
        return 'O'
    if board[0][2] == 'X' and board[1][1] == 'X' and board[2][0] == 'X':
        return 'X'
    if board[0][2] == 'O' and board[1][1] == 'O' and board[2][0] == 'O':
        return 'O'
    return None


playerstupid = 0
tictactoe = [
      [1,2,3],
      [4,5,6],
      [7,8,9]
      ]
x = input("welcome to tic tac toe please choose X or O: ")
if x == str("X"):
   b = str("O")
else:
   b = str("X")
game_active = True
while game_active:
   x == str(x)
   print("you will play as "+ x)
   time.sleep(1)
   print("pls pick a number from the grid to proced")
   time.sleep(1)
   print(tabulate(tictactoe, tablefmt='fancy_grid'))


   while playerstupid == 0:
    m = int(input("Enter a number (1-9): "))
    r = (m - 1) // 3 
    c = (m - 1) % 3 
    if tictactoe[r][c] != 'X' and tictactoe[r][c] != 'O':
     tictactoe[r][c] = x
     time.sleep(1)
     print(tabulate(tictactoe, tablefmt='fancy_grid'))
     if check_winner(tictactoe):
         print(f"Player {x} wins!")
         game_active = False
         break
     playerstupid = 5
     botstupid = 0
    else:
     time.sleep(1)
     print("position taken! Try again.")
     playerstupid = 0

   if not game_active:
     break

   time.sleep(1)
   print("BOT will play as "+ b)
   while botstupid == 0:
    m = random.randint(1, 9)
    r = (m - 1) // 3 
    c = (m - 1) % 3 
    if tictactoe[r][c] != 'X' and tictactoe[r][c] != 'O':
     tictactoe[r][c] = b
     time.sleep(1)
     print(tabulate(tictactoe, tablefmt='fancy_grid'))
     if check_winner(tictactoe):
         print(f"Bot {b} wins!")
         game_active = False
         break
     botstupid = 5
     playerstupid = 0
    else:
     botstupid = 0

is_draw = True
for row in tictactoe:
 for cell in row:
        if cell != 'X' and cell != 'O':  # If we find any number left
            is_draw = False
            break
 if not is_draw:
        break

 if is_draw:
    print("It's a draw!")
    game_active = False











