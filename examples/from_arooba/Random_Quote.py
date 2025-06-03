
from fastapi import FastAPI, Request
import uvicorn
import random

app = FastAPI()

quotes_db = [
    {
        "quote": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "category": "Inspiration"
    },
    {
        "quote": "Life is what happens when you're busy making other plans.",
        "author": "John Lennon",
        "category": "Life"
    }
]


@app.get("/get_random_quote")
def get_random_quote():
  return random.choice(quotes_db)

# Accept JSON body with POST
@app.post("/add_quote")
async def add_quote(request: Request):
    new_quote =  await request.json()
    quotes_db.append({
    "quote": new_quote["quote"],
    "author": new_quote["author"],
    "category": new_quote["category"]
})
    return {"message": "Quote added successfully", "quote": new_quote}

@app.get("/get_category_quotes")
def get_all_quotes(category: str):
    quotes_db_filtered = [
        quote for quote in quotes_db if quote["category"].lower() == category.lower()
    ]

    if not quotes_db_filtered:
        return {"message": f"No quotes found for category '{category}'"}

    return quotes_db_filtered

@app.get("/list_categories")
def list_categories():
    categories = {quote["category"] for quote in quotes_db}
    return {"categories": categories}

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8888)