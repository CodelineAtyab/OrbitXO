import random
import os
from fastapi import FastAPI
import uvicorn

random_api = "./examples/from_nabil/api.txt"

if not os.path.exists(random_api):
    print("file not found.")

def save_quote(quote, authoer, category):
    try:
        code_again = f"quote: {quote} - authoer: {authoer} - category: {category}"
        with open(random_api, "a") as f:
            f.write(code_again)
        return "successfully writien the quote"
    except FileNotFoundError:
        return "file not found {random_api}"


def fetch_random_quote():
    with open(random_api, "r" ) as f:
        lines_line  = f.readlines()
    random_line = random.choice(lines_line)
    return random_line


def find_quote(category):
    if not os.path.exists(random_api):
        return "file is not found. "
    with open(random_api, "r") as f:
        code_again = f.readlines()
    for line in code_again:
        parts = line.strip()
        if category.lower() in line.lower():
            return line.strip()
        return "category not found."


application  = FastAPI()

@application.post("/save_quote")
def save_to_quote(quote,auther,category):
    save_quote(quote, auther,category)
    return {"quote": quote, "auther" : auther , "category" : category}

@application.get("/category")
def category_find(category):
    return find_quote(category)

@application.get("/fetch_random_quote")
def random_quote():
    return fetch_random_quote()

if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=8888)
