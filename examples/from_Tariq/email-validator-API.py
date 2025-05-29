import fastapi
import re
import uvicorn

def is_valid_email(email):
    if not re.match(r'^[a-zA-Z0-9._%+-@]+$', email):
        return f"{email} has invalid characters."
    if '@' not in email:
        return f"{email} is missing an '@' character."
    if not re.search(r'@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return f"{email} has an invalid domain."
    return f"{email} is a valid email address."

app = fastapi.FastAPI()

@app.get("/validate-email/{email}")
def validate_email(email: str):
    message = is_valid_email(email)
    return {"message": message}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)