import uvicorn
import json
import secrets
from base64 import b64decode
from fastapi import FastAPI, Request

app = FastAPI()

auth_users = {
    "admin": "qwerty",
    "guest": "asdfgh"
}

@app.get("/")
def read_root(request: Request):
    headers = json.dumps(dict(request.headers))
    msg = {"status": "NOT PERMITTED!!!"}

    try:
      auth_header_value = request.headers.get("Authorization")
      encoded_user_pass = auth_header_value.split(" ")[1]
      decoded_user_pass = b64decode(encoded_user_pass).decode("utf-8")
      given_user, give_pass = decoded_user_pass.split(":")

      if given_user in auth_users and auth_users[given_user] == give_pass:
          msg["status"] = "PERMITTED!!!"

    except Exception as e:
        msg["status"] = "NOT PERMITTED!!!"

    print(f"Request Headers: {headers}")
    return msg

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)