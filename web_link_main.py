import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from main_app import perform_move, board

app = FastAPI()

# Add CORS middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # Allow all origins
  allow_credentials=True,
  allow_methods=["*"],  # Allow all methods
  allow_headers=["*"],  # Allow all headers
)

# API Endpoint - Function - Controller
@app.get("/make_move")
def make_move(move: str):
  return perform_move(move)


@app.get("/display_board")
def display_board():
  return board 


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8888)