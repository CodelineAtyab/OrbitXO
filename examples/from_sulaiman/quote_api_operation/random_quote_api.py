from fastapi import FastAPI
import random
import json
import hashlib
import uvicorn

app = FastAPI()

gaming_quotes_list = ["Don't wish it were easier. Wish you were better.",
                   "I don't need to get a life. I'm a gamer - I have lots of lives.",
                   "Life is a video game. No matter how good you get, you are always zapped in the end.",
                   "Every age has its storytelling form, and video gaming is a huge part of our culture.",
                   "Eat. Sleep. Game. Repeat.",
                   "Gaming brings people together."]

@app.get("/quotes/random")
def random_quote():
    try:
        file = open("examples/from_sulaiman/quote_api_operation/data.json", "r")
        lines = file.readlines()
        jlines = []
        for line in lines:
            jlines.append(json.loads(line))
        rand = random.choice(jlines)
        return f"ID:{rand["id"]}\n Quote:{rand["quote"]}\n Author:{rand["author"]}\n Category:{rand["category"]}"
    except json.JSONDecodeError:
        return "no quotes were entered"
    except FileNotFoundError:
        return "no quotes were entered"

@app.post("/quotes")
def post_quote(quote, author, category):
    file = open("examples/from_sulaiman/quote_api_operation/data.json", "a")
    unique_string = f"{quote}-{author}-{category}"
    id = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()
    json_data = {
        "id": id,
        "quote": quote,
        "author": author,
        "category": category
    }
    file.write(json.dumps(json_data) + "\n")
    file.close()
    return id, quote, author, category

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8567)