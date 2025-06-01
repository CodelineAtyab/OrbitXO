from fastapi import FastAPI, Body
import uvicorn
import re

app = FastAPI()

@app.post("/check-email")
def check_email(data: str ):
    if "@" not in data:
        return {"message": "@missing"}
    at_pos = data.find("@")
    dot_pos = data.rfind(".")
    if dot_pos < at_pos + 2:
        return {"message": "invalid domain"}
    if dot_pos >= len(data) - 2:
        return {"message": "Domain part after '.' is too short"}
    if data.count("@") != 1:
        return {"message": "Email should contain exactly one '@'"}
    return {"message": "Valid email format"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
