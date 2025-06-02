import random
import requests
import os
import fastapi as FastAPI
import uvicorn
import json

filepath = "./examples/from_almuhannad/randomQuote.json"


def get_random_quote():
#     try:
     with open(filepath,"r") as f:
          quotes = json.load(f)
     if not quotes:
      return "no quotes"
     random_quote = random.choice(quotes)
     return random_quote 
        

def save_quote(quote, auther, category):
     try:
        with open(filepath, "r") as f:
            quotes = json.load(f)
        new_quote = {
            "quote": quote,
            "author": auther,
            "category": category
        }
        quotes.append(new_quote)
        with open(filepath, "w") as f:
            json.dump(quotes, f, indent=2)
        print("Quote added successfully!")
     except Exception as ex:
         print(f"Error found {filepath}",ex)

def search_by_category(category):
     with open(filepath,"r") as f:
          quotes = json.load(f)
     match_quotes = []
     for quote in quotes:
         if category.lower() in quote["category"].lower():
            match_quotes.append(quote)
     if match_quotes:
               return match_quotes
     return "No quotes found in this category."
         

app = FastAPI.FastAPI()

@app.get("/random_quote")
def random_quote():
    return {"quote": get_random_quote()}

@app.post("/add_quote")
def add_quote(quote: str, author: str, category: str):
    save_quote(quote, author, category)
    return {
        "message": "Quote added successfully!",
        "quote": quote,
        "author": author,
        "category": category
    }
@app.get("/search_by_category")
def search_category(category):
    return{"qoute" : search_by_category(category)}

if __name__ == "__main__":
  
  if not os.path.exists(filepath):
        with open(filepath, "w") as file:
            json.dump([], file)
  uvicorn.run(app, host="0.0.0.0", port=8888)

