from fastapi import FastAPI
import random
import uvicorn

app = FastAPI()
quotes = []

@app.post("/quotes")
def add_quote(quote: str, author: str, category: str):
    new_quote = {
        "quote": quote,
        "author": author,
        "category": category
    }
    quotes.append(new_quote)
    return {"message": "Your quote added successfully"}

@app.get("/quotes/random")
def get_random_quote():
    if not quotes:
        return {"message": "No quotes available"}
    return random.choice(quotes)

@app.get("/quotes")
def get_quotes_by_category(category: str):
    matching = []
    for q in quotes:
        if category.lower() in q["category"].lower():
            matching.append(q)
    if matching:
        return matching
    return {"message": "No quotes found in this category"}

@app.get("/categories")
def list_categories():
    categories = []
    for q in quotes:
        if q["category"] not in categories:
            categories.append(q["category"])
    return {"categories": categories}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)