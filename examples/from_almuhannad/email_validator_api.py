import re
import fastapi as FastAPI
import uvicorn

pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

def validate_email(email):
    if not "@" in email:
        return f"{email} is missing "@""
    if not "." in email:
        return f"{email} is missing domain"
    if not re.fullmatch(pattern, email):
        return f"{email} has an invalid format"
    return f"{email} is a valid email"

app = FastAPI.FastAPI()

@app.post("/validate_email")
def is_a_valid_email(email):
    message = validate_email(email)
    return "Message",message

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)


