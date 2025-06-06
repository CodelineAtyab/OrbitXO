import fastapi
import uvicorn
import random

import json
import os

app = fastapi.FastAPI()

quotes = []

@app.post("/quotes")
def add_quote( quote: str,author: str,category: str):
    
    if os.path.exists("quotes.json"):
        with open("quotes.json", "r") as f:
            quotes = json.load(f)
    else:
        quotes = []

    new_quote = {
        "id": len(quotes) + 1,
        "quote": quote,
        "author": author,
        "category": category
    }
    quotes.append(new_quote)

    with open("quotes.json", "w") as f:
        json.dump(quotes, f, indent=2)
    return {"id": new_quote["id"], "message": "Quote added successfully"}

@app.get("/quotes/random")
def get_random_quote():
    if os.path.exists("quotes.json"):
        with open("quotes.json", "r") as f:
            quotes = json.load(f)
    else:
        return {"message": "No quotes"}
    selected = random.choice(quotes)
    return  {"quote": selected["quote"],"author":selected["author"] ,"category": selected["category"] }


@app.get("/quotes")
def get_quotes_by_category(category=None):
    if os.path.exists("quotes.json"):
        with open("quotes.json", "r") as f:
            quotes = json.load(f)
    else:
        return {"message": "No quotes available."}

    if category:
        filtered = [q for q in quotes if q["category"].lower() == category.lower()]
        if not filtered:
            return {"message": f"No quotes found for category '{category}'"}
        return filtered

    return quotes



@app.get("/categories")
def list_categories():
    if os.path.exists("quotes.json"):
        with open("quotes.json", "r") as f:
            quotes = json.load(f)
    else:
        return {"message": "No quotes available."}

    categories = set()
    for q in quotes:
        categories.add(q["category"].strip().lower())

    return {"categories": categories}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)