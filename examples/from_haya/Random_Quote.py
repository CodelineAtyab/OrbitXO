import random
import fastapi
import uvicorn
import os
import hashlib

DATA_FILE = "examples/from_haya/quotes_data.txt"

def save_quote(title_text, quote_text, quote_category):
    quote_id = hashlib.md5(quote_text.encode()).hexdigest()
    entry = f"{quote_id} | {title_text} | {quote_text} | {quote_category}\n"
    with open(DATA_FILE, "a") as file:
        file.write(entry)
    print("Quote has been saved.")

def get_random_quote():
    if not os.path.exists(DATA_FILE):
        return "No quotes found."
    with open(DATA_FILE, "r") as file:
        all_quotes = file.readlines()
    if not all_quotes:
        return "No quotes available."
    return random.choice(all_quotes).strip()

def search_quote_by_category(search_category):
    if not os.path.exists(DATA_FILE):
        return "Quote file not found."
    with open(DATA_FILE, "r") as file:
        quote_records = file.readlines()
    for record in quote_records:
        parts = record.strip().split("|")
        if len(parts) == 4 and search_category.lower() in parts[3].lower():
            return record.strip()
    return "No matching category found."

app = fastapi.FastAPI()

@app.post("/create-quote")
def create_quote(title: str, content: str, category: str):
    save_quote(title, content, category)
    return {"status": "Quote added successfully"}

@app.get("/random")
def random_quote():
    return {"quote": get_random_quote()}

@app.get("/category-search")
def category_search(category: str):
    return {"result": search_quote_by_category(category)}

if __name__ == "__main__":
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            file.write("")
    uvicorn.run(app, host="0.0.0.0", port=8888)
