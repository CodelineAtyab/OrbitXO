import uvicorn
import json
from fastapi import FastAPI, Request

app = FastAPI()

auth_users = {"admin": "Zack Zuckleburg", "user1": "Lex Luther"}

@app.get("/")
def read_route(request: Request):
    headers = json.dumps(dict(request.headers))
    print(request.headers)
    # auth_header = request.headers.get("Authorization")
    # if auth_header:
    #     auth_token = auth_header.split(" ")[1]
    return {"SecretMessage": "This is a secret message"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
