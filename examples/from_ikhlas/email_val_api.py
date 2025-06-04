import fastapi
import re
import uvicorn

email_regex_pattern= re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

app= fastapi.FastAPI()

def email_valid(email: str=""):
    
    if not email:
        return {"is_valid" : False, "message": "No provided email"}
    
    if "@" not in email:
        return {"is_valid" : False, "message": "Invalid format, @ symbol is missing"}
    
    email_domain=email.split("@")[-1]

    if email_domain.startswith(".") or email_domain.endswith("."):
        return {"is_valid": False, "message": "Email domain cannot start or end with dot."}

    if not email_regex_pattern.fullmatch(email):
        return {"is_valid": False, "message": "Invalid email format."}

    return {"is_valid": True, "message": "Email address is valid"}

@app.get("/validate-email")

def validate_email(email: str = ""):
    return email_valid(email)

if __name__ == "__main__":
    uvicorn.run("email_val_api:app", host="localhost", port=8888, reload=True)

