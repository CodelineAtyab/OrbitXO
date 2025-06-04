from fastapi import FastAPI
import re
import uvicorn

app = FastAPI()

def is_valid_email(email): 
    #This part to ensure the email have the allowed characters
    if not re.match(r'^[a-zA-Z0-9._%+-@]+$', email): #re. regex format and ^ means from the start
        return "Email has invalid characters."

    if '@' not in email:
        return "Email is missing '@'."
    
    #This part to check the email has domain part correctly
    if not re.search(r'@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return "Email has an invalid domain."

    #This part if all checks passed
    return "Email is valid."

# Create an API route to validate the email
@app.get("/check-email/{email}")
def check_email(email: str):
    result = is_valid_email(email)
    return {"message": result}

# Run the app if this file is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
