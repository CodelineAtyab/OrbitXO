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
if os.path.isfile(file_name):
    with open(file_name, "r") as file:
        try:
            my_quotes = json.load(file)
        except:
            my_quotes = []  # start fresh if file is broken

# Function to save quotes to the file
def write_quotes():
    with open(file_name, "w") as file:
        json.dump(my_quotes, file, indent=4)

# Add a new quote
@app.post("/quotes")
def create_quote(quote: str, author: str, category: str):
    q = {
        "quote": quote,
        "author": author,
        "category": category
    }
    my_quotes.append(q)
    write_quotes()
    return {"message": "Quote added!"}

# Get a random quote
@app.get("/quotes/random")
def random_quote():
    if len(my_quotes) == 0:
        return {"message": "No quotes yet."}
    return random.choice(my_quotes)

# Get quotes by category
@app.get("/quotes")
def filter_quotes(category: str):
    result = []
    for q in my_quotes:
        if category.lower() in q["category"].lower():
            result.append(q)
    if len(result) == 0:
        return {"message": "No quotes in that category."}
    return result

# List all categories
@app.get("/categories")
def show_categories():
    cat_set = set()
    for q in my_quotes:
        cat_set.add(q["category"])
    return {"categories": list(cat_set)}

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
