# Import necessary modules
import fastapi   # FastAPI for building the web API
import re        # re for regular expression matching
import uvicorn   # uvicorn for running the FastAPI app

# Function to validate an email address using regex
def is_valid_email(email):
    # Check for invalid characters in the email
    if not re.match(r'^[a-zA-Z0-9._%+-@]+$', email):
        return f"{email} has invalid characters."
    
    # Check if email contains the '@' symbol
    if '@' not in email:
        return f"{email} is missing an '@' character."
    
    # Check if email has a valid domain (e.g., @domain.com)
    if not re.search(r'@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return f"{email} has an invalid domain."
    
    # If all checks pass, the email is valid
    return f"{email} is a valid email address."

# Create a FastAPI application instance
app = fastapi.FastAPI()

# Define an endpoint to validate the email address
@app.get("/validate-email/{email}")
def validate_email(email: str):
    message = is_valid_email(email)
    return {"message": message}

# Run the application using Uvicorn (only if executed directly)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
