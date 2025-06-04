import random
import fastapi
import os
import uvicorn

file_path="C:/Users/admin/Desktop/quote_task.txt" 

app=fastapi.FastAPI()

def add_new_quote(quote:str, author:str, category:str):
    with open(file_path, "a") as file:
        file.write(f"{quote} - {author} - {category}\n")


def call_random_quote():
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return "No quotes available"
    with open(file_path, "r") as file:
        quotes=file.readlines()
    return random.choice(quotes).strip()


def search_quote_by_category(category: str): 
    with open(file_path, "r") as file:
        quotes=file.readlines()
        for q in quotes:
            if q.strip().endswith(category):
                return q.strip()
        return "No quotes found in this category"

@app.get("/random-quote")
def random_quote():
    return {"quote": call_random_quote()}

@app.post("/add-quote")
def add_quote(quote:str, author:str, category:str):
    add_new_quote(quote, author, category)
    return {"message": "Quote added successfully"}

@app.get("/search-quote")
def search_quote(category: str):
    return {"quotes": search_quote_by_category(category)}

# Run the app
if __name__ == "__main__":
    if not os.path.exists(file_path):
       with open(file_path, "w") as file:
           file.write("")
    uvicorn.run(app, host="0.0.0.0", port=8888)