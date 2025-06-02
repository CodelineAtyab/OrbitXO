from fastapi import FastAPI, Request
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
async def validate_email(request: Request):
    data = await request.json()
    email = data.get("email")

    if not email:
        return {
            "is_valid": False,
            "message": "Missing 'email' field in the request body"
        }

    is_valid, message = validate_email_format(email)
    return {
        "is_valid": is_valid,
        "message": message
    }


if __name__ == "__main__":
    uvicorn.run("email_validator:app", host="127.0.0.1", port=8000, reload=True)
