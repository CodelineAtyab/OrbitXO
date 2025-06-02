import fastapi
import re
import uvicorn

pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
app = fastapi.FastAPI()

def is_valid_email(email):

    if not email:
        return {"is_valid": False, "message": "No email provided."}
    
    if '@' not in email:
        return  {"is_valid": False, "message": "Invalid email format. Missing @ symbol."}
    
    if '.' not in email.split('@')[-1]:
        return {"is_valid": False, "message": "Invalid email format. Missing domain suffix"}
    
    if not re.match(pattern, email):
         return {"is_valid": False, "message": "Invalid email format. Please check for invalid characters or structure."}

    return {"is_valid": True, "message": "Email address is valid"}

@app.get("/validate-email/{email}")

def validate_email(email: str):
    return is_valid_email(email)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)