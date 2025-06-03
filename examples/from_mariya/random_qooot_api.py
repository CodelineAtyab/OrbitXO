from fastapi import FastAPI
import random
import uvicorn
import json
import os

app = FastAPI()
quotes_file = "quotes.json"
quotes = []

# Load quotes from JSON file at startup
if os.path.exists(quotes_file):
    with open(quotes_file, "r") as f:
        try:
            quotes = json.load(f)
        except json.JSONDecodeError:
            quotes = []

# Save quotes to JSON file
def save_quotes():
    with open(quotes_file, "w") as f:
        json.dump(quotes, f, indent=4)

@app.post("/quotes")
def add_quote(quote: str, author: str, category: str):
    new_quote = {
        "quote": quote,
        "author": author,
        "category": category
    }
    quotes.append(new_quote)
    save_quotes()
    return {"message": "Your quote was added successfully."}

@app.get("/quotes/random")
def get_random_quote():
    if not quotes:
        return {"message": "No quotes available"}
    return random.choice(quotes)

@app.get("/quotes")
def get_quotes_by_category(category: str):
    matching = [q for q in quotes if category.lower() in q["category"].lower()]
    if matching:
        return matching
    return {"message": "No quotes found in this category"}

@app.get("/categories")
def list_categories():
    categories = list(set(q["category"] for q in quotes))
    return {"categories": categories}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
