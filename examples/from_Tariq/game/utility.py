import uuid

boards = {}


def create_uuid():
    return str(uuid.uuid4())

def create_board(board_id):
    boards[board_id] = {"board": [["", "", ""], ["", "", ""], ["", "", ""]], "count": 0}
    return boards[board_id]["board"]

def get_board(board_id):
    if board_id in boards:
        return boards[board_id]["board"]
    return None

def is_valid():
    return True

def turn(board_id):
    count = boards[board_id]["count"]
    if count % 2 == 0:
        if is_valid():
         boards[board_id]["count"] += 1
        return "X"
    elif count % 2 == 1:
        if is_valid():
         boards[board_id]["count"] += 1
        return "O"
    