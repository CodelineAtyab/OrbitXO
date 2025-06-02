import random
import fastapi
import uvicorn
import os
import hashlib

QUOTE_FILE = "./quote.txt"

def store_quote(content, writer, tag):
    unique_id = hashlib.md5(content.encode()).hexdigest()
    record = f"{unique_id} | {content} | {writer} | {tag}\n"
    with open(QUOTE_FILE, "a", encoding="utf-8") as f:
        f.write(record)
    print("Quote saved.")

def fetch_random_quote():
    if not os.path.exists(QUOTE_FILE):
        return "Quote file not found."
    with open(QUOTE_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        return "No quotes stored yet."
    return random.choice(lines).strip()

def find_quote_by_tag(tag):
    if not os.path.exists(QUOTE_FILE): 
        return "Quote file is missing."
    with open(QUOTE_FILE, "r", encoding="utf-8") as f:
        records = f.readlines()
    for line in records:
        parts = line.strip().split("|")
        if len(parts) == 4 and tag.lower() in parts[3].lower():
            return line.strip()
    return "No matching tag found."

app = fastapi.FastAPI()

@app.post("/insert")
def insert(content: str, writer: str, tag: str):
    store_quote(content, writer, tag)
    return {"status": "Quote successfully stored."}


@app.get("/random")
def random_quote():
    return {"quote": fetch_random_quote()}

@app.get("/category")
def category_search(tag: str):
    return {"result": find_quote_by_tag(tag)}


if __name__ == "__main__":
    if not os.path.exists(QUOTE_FILE):
        with open(QUOTE_FILE, "w", encoding="utf-8") as f:
            f.write("")
    uvicorn.run(app, host="0.0.0.0", port=8888)
