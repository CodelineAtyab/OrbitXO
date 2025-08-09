#!/usr/bin/env python3
"""
Simple test script to demonstrate the Tic-Tac-Toe API usage.

This script shows how to interact with the API to create games,
join players, make moves, and check scores.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def pretty_print(response):
    """Pretty print JSON response."""
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

def main():
    """Demonstrate API usage with a complete game."""
    print("=== Tic-Tac-Toe API Demo ===\n")
    
    # 1. Check API status
    print("1. Checking API status...")
    response = requests.get(f"{BASE_URL}/")
    pretty_print(response)
    
    # 2. Create a new game
    print("2. Creating a new game...")
    game_data = {"creator_name": "Alice"}
    response = requests.post(f"{BASE_URL}/games", json=game_data)
    pretty_print(response)
    game_id = response.json()["data"]["game_id"]
    
    # 3. Join the game
    print("3. Bob joins the game...")
    join_data = {"player_name": "Bob"}
    response = requests.post(f"{BASE_URL}/games/{game_id}/join", json=join_data)
    pretty_print(response)
    
    # 4. Check game state
    print("4. Checking initial game state...")
    response = requests.get(f"{BASE_URL}/games/{game_id}")
    pretty_print(response)
    players = response.json()["players"]
    alice_id = next(p["player_id"] for p in players if p["player_name"] == "Alice")
    bob_id = next(p["player_id"] for p in players if p["player_name"] == "Bob")
    
    # 5. Play the game
    print("5. Playing the game...")
    moves = [
        (alice_id, 0, 0, "Alice plays X at (0,0)"),
        (bob_id, 1, 1, "Bob plays O at (1,1)"),
        (alice_id, 0, 1, "Alice plays X at (0,1)"),
        (bob_id, 1, 0, "Bob plays O at (1,0)"),
        (alice_id, 0, 2, "Alice plays X at (0,2) - WINS!")
    ]
    
    for player_id, row, col, description in moves:
        print(f"   {description}")
        move_data = {"player_id": player_id, "row": row, "col": col}
        response = requests.post(f"{BASE_URL}/games/{game_id}/move", json=move_data)
        pretty_print(response)
        
        # Stop if game is over
        if response.json().get("data", {}).get("game_over"):
            break
    
    # 6. Check final game state
    print("6. Checking final game state...")
    response = requests.get(f"{BASE_URL}/games/{game_id}")
    pretty_print(response)
    
    # 7. Get final score
    print("7. Getting final score...")
    response = requests.get(f"{BASE_URL}/games/{game_id}/score")
    pretty_print(response)
    
    # 8. Try to make a move on completed game (should fail)
    print("8. Trying to make a move on completed game (should fail)...")
    try:
        move_data = {"player_id": bob_id, "row": 2, "col": 2}
        response = requests.post(f"{BASE_URL}/games/{game_id}/move", json=move_data)
        print(f"Status: {response.status_code}")
        pretty_print(response)
    except Exception as e:
        print(f"Error: {e}")
    
    print("=== Demo Complete ===")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Please make sure the server is running with: uvicorn main:app --reload")
    except Exception as e:
        print(f"Error: {e}")