import uuid

game={}


def uuid_create():  #create the uuid
    return str(uuid.uuid4())

def board_creation(board_id):
    board = [["","",""],
             ["","",""],
             ["","",""]]
         
    game[board_id]= board
    return board

