from fastapi import FastAPI
import uvicorn
import re

def check_email(email):
    pattern = r'^[a-zA-Z0-9._%+-@]+$'
    pattern_after_at = r'@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return f"{email} has invalid charecters"
    if '@' not in email:
        return f"{email} is missing @"
    if not re.match(pattern_after_at, email[email.index("@"):]):
        return f"{email} invalid domain"
    return f"{email} is valid"


app = FastAPI()

@app.get("/validate")
def validate(email):
    message = check_email(email)
    return  message

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4444)


