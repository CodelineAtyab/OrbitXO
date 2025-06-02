from fastapi import FastAPI, Body
import uvicorn

app = FastAPI()

@app.post("/check-email")
def check_email(data: str ):
    if not data or data[0] in ["@", "."]:
        return {"message": "Email must start with a valid word, not '@' or '.'"}
    if "@" not in data:
        return {"is_valid": False, "message": "Email must contain '@'"}
    at_pos = data.find("@")
    dot_pos = data.rfind(".")
    if dot_pos < at_pos + 2 or dot_pos >= len(data) - 2:
        return {"valid": False, "message": "Invalid domain part"}
    return {"message": "Valid email format"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)