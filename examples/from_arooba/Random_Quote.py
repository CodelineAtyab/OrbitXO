import random
import fastapi
import uvicorn
import os
import hashlib

QUOTE_FILE = "./quote.txt"

def store_quote(title, content, category):
    unique_id = hashlib.md5(content.encode()).hexdigest()
    record = f"{unique_id} | {title} | {content} | {category}\n"
    with open(QUOTE_FILE, "a", encoding="utf-8") as f:
        f.write(record)
    print("quote saved.")

def fetch_random_quote():
    if not os.path.exists(QUOTE_FILE):
        return "No quotes found."
    with open(QUOTE_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        return "No quotes available."
    return random.choice(lines).strip()

def find_quote_by_category(category):
    if not os.path.exists(QUOTE_FILE):
        return "Quote file missing."
    with open(QUOTE_FILE, "r", encoding="utf-8") as f:
        records = f.readlines()
    for line in records:
        parts = line.strip().split("|")
        if len(parts) == 4 and category.lower() in parts[3].lower():
            return line.strip()
    return "No matching category found."

app = fastapi.FastAPI()

@app.post("/add-quote")
def add_quote(title: str, content: str, category: str):
    store_quote(title, content, category)
    return {"status": "Quote successfully stored"}

@app.get("/random-quote")
def get_random_quote():
    return {"quote": fetch_random_quote()}

@app.get("/search-category")
def search_by_category(category: str):
    return {"result": find_quote_by_category(category)}

if __name__ == "__main__":
    if not os.path.exists(QUOTE_FILE):
        with open(QUOTE_FILE, "w", encoding="utf-8") as f:
            f.write("")
    uvicorn.run(app, host="0.0.0.0", port=8888)