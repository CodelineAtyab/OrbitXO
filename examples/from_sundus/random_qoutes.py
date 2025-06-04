from fastapi import FastAPI, Form
import random
import uvicorn
import os

app = FastAPI()

file_path = os.path.join(os.path.dirname(__file__), "random_quotes.txt")


quotes = []

# Load quotes from the file
def load_quotes():
    loaded_quotes = []
    if not os.path.exists(file_path):
        open(file_path, "w").close()  # Create file if not exists
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 4:
                    quote = {
                        "id": int(parts[0]),
                        "quote": parts[1],
                        "author": parts[2],
                        "category": parts[3]
                    }
                    loaded_quotes.append(quote)
    except Exception as e:
        print(f"Error loading quotes: {e}")
    return loaded_quotes


def save_quotes():
    try:
        with open(file_path, "w") as file: 
            for q in quotes:
                line = f"{q['id']}|{q['quote']}|{q['author']}|{q['category']}\n"
                file.write(line)
        print(f"Saved {len(quotes)} quotes to {file_path}")
    except Exception as e:
        print(f"Error saving quotes: {e}") 

# Get next unique ID
def get_next_id():
    return max([q["id"] for q in quotes], default=0) + 1

# Load quotes when the app starts
quotes = load_quotes()

# Add a new quote
@app.post("/quotes")
def add_quote(quote: str = Form(...), author: str = Form(...), category: str = Form(...)):
    new_id = get_next_id()
    quote_data = {
        "id": new_id,
        "quote": quote,
        "author": author,
        "category": category
    }
    quotes.append(quote_data)
    save_quotes()
    return {"id": new_id, "message": "Quote added successfully"}

# Get a random quote
@app.get("/quotes/random")
def get_random_quote():
    if not quotes:
        return {"message": "No quotes available yet"}
    return random.choice(quotes)

# Get quotes by category
@app.get("/quotes/category/{category_name}")
def get_quotes_by_category(category_name: str):
    result = [quote for quote in quotes if quote["category"].lower() == category_name.lower()]
    if not result:
        return {"message": "No quotes found in this category"}
    return result

# List all categories
@app.get("/quotes/categories")
def list_categories():
    category_list = list(set(q["category"] for q in quotes))
    return {"categories": category_list}

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8888)


