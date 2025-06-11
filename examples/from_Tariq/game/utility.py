import uuid

boards = {}

def create_uuid():
    return str(uuid.uuid4())

def create_board(board_id):
    boards[board_id] = [["", "", ""], ["", "", ""], ["", "", ""]]
    return boards[board_id]
