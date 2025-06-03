from fastapi import FastAPI, Form
import re
import uvicorn

app = FastAPI() 

def validate_email_format(email: str):
    if "@" not in email:
        return False, "Invalid email format. Missing @ symbol."
    if "." not in email.split("@")[-1]:
        return False, "Invalid email format. Missing domain extension (e.g., .com)."
    

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        return False, "Invalid email format. Regex check failed."

    return True, "Email address is valid"

@app.post("/validate-email")
def validate_email(email: str = Form(...)):
    is_valid, message = validate_email_format(email)
    return {
        "is_valid": is_valid,
        "message": message
    }


if __name__ == "__main__":
    uvicorn.run("email_validator:app", host="localhost", port=8888, reload=True)
