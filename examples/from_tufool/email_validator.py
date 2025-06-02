from fastapi import FastAPI, Request
import re
import uvicorn

app = FastAPI()

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

# ^ means “start of the string”
# [\w\.-]+ means “one or more letters, numbers, dot or dash”
# @ means the literal @ symbol
# \. means a literal dot .
# $ means “end of the string”
# json = { "email": "example@domain.com" }

@app.post("/validate-email")
async def validate_email(request: Request):  
    try:
        data = await request.json()  
    except:
        return {
            "is_valid": False,
            "message": "Invalid request format. Please send a JSON with an email field."
        }

    email = data.get("email")
    if not email:
        return {"is_valid": False, "message": "Email address is missing."}

    # Email format checks
    if not re.match(EMAIL_REGEX, email):
        if '@' not in email:
            return {"is_valid": False, "message": "Invalid email format. Missing @ symbol."}
        elif email.count('@') > 1:
            return {"is_valid": False, "message": "Invalid email format. More than one @ symbol."}
        elif '.' not in email.split('@')[1]:
            return {"is_valid": False, "message": "Invalid email format. Missing domain dot (e.g. .com)."}
        else:
            return {"is_valid": False, "message": "Invalid email format."}

    return {"is_valid": True, "message": "Email address is valid"}

if __name__ == "__main__":
    uvicorn.run("email_validator:app", host="127.0.0.1", port=8000, reload=True)
