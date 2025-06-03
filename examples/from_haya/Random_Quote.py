from fastapi import FastAPI, HTTPException, Body
import random

app = FastAPI()
quotes_db = []

@app.post("/quotes")
def add_quote(quote_data: dict = Body(...)):
    quote_id = len(quotes_db) + 1
    new_quote = {
        "id": quote_id,
        "quote": quote_data["quote"],
        "author": quote_data["author"],
        "category": quote_data["category"]
    }
    quotes_db.append(new_quote)
    return {"id": quote_id, "message": "Quote added successfully"}

@app.get("/quotes/random")
def get_random_quote():
    if not quotes_db:
        raise HTTPException(status_code=404, detail="No quotes available")
    return random.choice(quotes_db)

@app.get("/quotes/category/{category_name}")
def get_quotes_by_category(category_name: str):
    filtered_quotes = [q for q in quotes_db if q["category"].lower() == category_name.lower()]
    if not filtered_quotes:
        raise HTTPException(status_code=404, detail="No quotes found in this category")
    return filtered_quotes

@app.get("/quotes/categories")
def get_categories():
    categories = list(set(q["category"] for q in quotes_db))
    return {"categories": categories}
