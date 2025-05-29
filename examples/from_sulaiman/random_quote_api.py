from fastapi import FastAPI
import random

app = FastAPI()

gaming_quotes_list = ["Don't wish it were easier. Wish you were better.",
                   "I don't need to get a life. I'm a gamer - I have lots of lives.",
                   "Life is a video game. No matter how good you get, you are always zapped in the end.",
                   "Every age has its storytelling form, and video gaming is a huge part of our culture.",
                   "Eat. Sleep. Game. Repeat.",
                   "Gaming brings people together."]

@app.get("/quotes/random")
def random_quote():
    random.choice(gaming_quotes_list)

@app.post("/quotes")
def post_quote(quote, author, category):
    pass