import fastapi
import uvicorn
import random

app = fastapi.FastAPI()

quotes = []
data_file = "quotes.txt"

def save_quote_to_file(quote: str, author: str, category: str):
    with open(data_file, "a", encoding="utf-8") as f:
        f.write(f"{quote}\n{author}\n{category}\n")

def load_quotes():
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            for i in range(0, len(lines), 3):
                if i + 2 < len(lines):
                    quote = lines[i].strip()
                    author = lines[i+1].strip()
                    category = lines[i+2].strip()
                    quotes.append({
                        "id": len(quotes) + 1,
                        "quote": quote,
                        "author": author,
                        "category": category
                    })
    except:
        pass  # If file doesn't exist yet, ignore

load_quotes()

@app.post("/quotes")
async def add_quote(quote_data: dict):
    # Expect JSON body with keys: quote, author, category
    quote_text = quote_data.get("quote", "").strip()
    author = quote_data.get("author", "").strip()
    category = quote_data.get("category", "").strip()
    
    if not quote_text or not author or not category:
        return {"error": "quote, author, and category are required."}
    
    new_quote = {
        "id": len(quotes) + 1,
        "quote": quote_text,
        "author": author,
        "category": category
    }
    quotes.append(new_quote)
    save_quote_to_file(quote_text, author, category)
    return {"id": new_quote["id"], "message": "Quote added successfully"}

@app.get("/quotes/random")
def get_random_quote():
    if not quotes:
        return {"error": "No quotes available."}
    return random.choice(quotes)

@app.get("/quotes/category/{category}")
def get_quotes_by_category(category: str):
    filtered = [q for q in quotes if q["category"].lower() == category.lower()]
    if not filtered:
        return {"error": "No quotes in this category."}
    return filtered

@app.get("/categories")
def list_categories():
    categories = list(set(q["category"] for q in quotes))
    return {"categories": categories}

if __name__ == "__main__":
    uvicorn.run("random_quote:app", host="127.0.0.1", port=8000, reload=True)

