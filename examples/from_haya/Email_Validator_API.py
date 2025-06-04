from fastapi import FastAPI, Body
import uvicorn

app = FastAPI() # This line tells FastAPI to use the function below for POST requests to /check-email
@app.post("/check-email") #@ is a decorator this will oprate when the user 
def validate_email(email: str):

    if " " in email:
        return {"is_valid": False, "message": "Email must not contain spaces"}  # Check for any spaces in the email

    if "@" not in email:
        return {"is_valid": False, "message": "Email must contain '@' symbol"}  # Check if '@' is present

    if not email or email[0] in ["@", "."]:    # Check if email is empty or starts with invalid characters
        return {"is_valid": False, "message": "Email must start with a valid character, not '@' or '.'"}

    at_index = email.find("@")
    last_dot_index = email.rfind(".")

    if at_index < 3: # Check local part length (before '@')
        return {"is_valid": False, "message": "The part before '@' must be at least 3 characters long"}

    if last_dot_index < at_index + 2 or last_dot_index >= len(email) - 2:
        return {"is_valid": False, "message": "Invalid domain part after '@'"} # Check position of '.' relative to '@' and end of string

    return {"is_valid": True, "message": "Valid email format"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)

