import random
import fastapi
import uvicorn
import os
import hashlib
import json

FILE_PATH = ".\quotes.json"


def add_new_quote(quote, author, category):

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            quotes = json.load(file)
    else:
        quotes = []
    id = hashlib.md5(quote.encode()).hexdigest()
    new_quote = {
        "id": id,
        "quote": quote,
        "author": author,
        "category": category
        }
    quotes.append(new_quote)
    with open(FILE_PATH, "w") as file:
        json.dump(quotes, file, indent=2)
    print("New quote added successfully!")

def get_random_quote():
    with open(FILE_PATH, "r") as file:
        quotes = json.load(file)
    if not quotes:
        return "No quotes available."
    random_quote = random.choice(quotes)
    return random_quote

def search_quotes_by_category(category):
    with open(FILE_PATH, "r") as file:
            quotes = json.load(file)
    matching_quotes = []
    for quote in quotes:
        if category.lower() in quote["category"].lower():
            matching_quotes.append(quote)
    if matching_quotes:
        return matching_quotes
    return "No quotes found in this category."

app = fastapi.FastAPI()
@app.get("/random-quote")
def random_quote():
    return {"quote": get_random_quote()}
@app.post("/add-quote")
def add_quote(quote, author, category):
    add_new_quote(quote, author, category)
    return {"message": "Quote added successfully!"}
@app.get("/search-quote")
def search_quote(category):
    return {"quote": search_quotes_by_category(category)}

if __name__ == "__main__":
  
  if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as file:
            json.dump([], file)
  uvicorn.run(app, host="0.0.0.0", port=8888)