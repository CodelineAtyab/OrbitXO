from fastapi import FastAPI
import random
import uvicorn
import json
import os

app = FastAPI()

# File to save and load the quotes
file_name = "quotes.json"

# Quotes will be stored in this list
my_quotes = []

# Try to load existing quotes from file
if os.path.exists(file_name):
    with open(file_name, "r") as file:
        try:
            my_quotes = json.load(file)
        except json.JSONDecodeError:
            my_quotes = []  # start fresh if file is broken

# Function to save quotes to the file
def save_quotes():
    with open(file_name, "w") as file:
        json.dump(my_quotes, file, indent=4)

# Add a new quote
@app.post("/quotes")
def add_quote(quote: str, author: str, category: str):
    q = {
        "quote": quote,
        "author": author,
        "category": category
    }
    my_quotes.append(q)
    add_quote()
    return {"message": "Quote added!"}

# Get a random quote
@app.get("/quotes/random")
def random_quote():
    if not my_quotes:
        return {"message": "No quotes yet."}
    return random.choice(my_quotes)

# Get quotes by category
@app.get("/quotes")
def filter_quotes(category: str):
    matching = [q for q in my_quotes if category.lower() in q["category"].lower()]
    if matching:
        return matching
    return {"message": "No quotes in that category."}

# List all categories
@app.get("/categories")
def list_categories():
    categories = list(set(q["category"]for q in my_quotes))
    return {"categories": categories}

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
