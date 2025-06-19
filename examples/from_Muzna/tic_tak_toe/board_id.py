import uuid
from games_store import all_games  
# Generate a random UUID (v4)
# random_uuid = uuid.uuid4()
# print(random_uuid)

activ_player='x'


def create_new_board():
    board_id = str(uuid.uuid4())
    
    # Initialize a 3x3 empty board
    empty_board = [ ["" for j in range(3)] for i in range(3)]

    # Store the board with metadata
    all_games[board_id] = {
        "board": empty_board 
    }

    return board_id




if __name__ == "__main__":
    #empty_board = [ ["" for j in range(3)] for i in range(3)]
    #print(empty_board)
    new_id = create_new_board()
    print(f"Na new board with ID: {new_id}")
    print("all boarders")
    print(all_games)
