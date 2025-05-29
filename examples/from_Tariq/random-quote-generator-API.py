import random
import fastapi
import uvicorn
import os
import hashlib

FILE_PATH = ".\quotes.txt"


def add_new_quote(quote, author, category):

    with open(FILE_PATH, "a") as file:
        id = hashlib.md5(quote.encode()).hexdigest()
        file.write(f"{id} - {quote} - {author} - {category}\n")
    print("New quote added successfully!")

def get_random_quote():
    with open(FILE_PATH, "r") as file:
        quotes = file.readlines()
    if not quotes:
        return "No quotes available."
    random_quote = random.choice(quotes).strip()
    return random_quote

def search_quotes_by_category(category):
    with open(FILE_PATH, "r") as file:
        quotes = file.readlines()
    for quote in quotes:
        if category.lower() in quote.lower():
            return quote.strip()
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
            file.write("")
  uvicorn.run(app, host="0.0.0.0", port=8888)