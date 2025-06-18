# tic_tac_toe.py
from flask import Flask, jsonify
import uuid
import threading

app = Flask(__name__)

# Thread-safe in-memory storage for game boards
class GameStore:
    def __init__(self):
        self._games = {}
        self._lock = threading.Lock()

    def create(self, board_id: str, state: dict):
        with self._lock:
            self._games[board_id] = state

    def get(self, board_id: str):
        with self._lock:
            return self._games.get(board_id)

store = GameStore()

def new_board():
    """Initialize an empty 3×3 board."""
    return [["" for _ in range(3)] for _ in range(3)]

@app.route('/board', methods=['POST'])
def create_board():
    # Generate a random UUIDv4 as game ID
    board_id = str(uuid.uuid4())  # uuid4 generates a random UUID :contentReference[oaicite:1]{index=1}
    state = {
        "board": new_board(),
        "active_player": "X"
    }
    store.create(board_id, state)
    return jsonify({"board_id": board_id}), 201

@app.route('/board/<uuid:board_id>', methods=['GET'])
def get_board(board_id):
    # Flask’s uuid converter ensures valid UUID format :contentReference[oaicite:2]{index=2}
    board_id_str = str(board_id)
    state = store.get(board_id_str)
    if state is None:
        return jsonify({"error": "Board not found"}), 404
    return jsonify(state), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

