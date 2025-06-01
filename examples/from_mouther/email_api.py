from fastapi import FastAPI, Request
import uvicorn


app = FastAPI()


@app.post("/validate_email")
def validate_email(email: str): 
    if "@" not in email:
        return {"message": "Invalid email address: missing '@'"}
    elif "." not in email:
        return {"message": "Invalid email address: missing '.'"}
    elif email.index("@") > email.index("."):
        return {"message": "Invalid email address: '@' must come before '.'"}
    elif email.index("@") <= 0:
        return {"message": "Invalid email address: '@' must not be the first character"}
    elif email.index(".") >= len(email) - 1:
        return {"message": "Invalid email address: '.' must not be the last character"}
    elif email.index(".") - email.index("@") <= 1:
        return {"message": "Invalid email address: there must be at least one character between '@' and '.'"}
    elif email.count("@") != 1:
        return {"message": "Invalid email address: '@' must appear exactly once"}
    elif len(email[email.rindex(".")+1:]) <= 2:
        return {"message": "Invalid email address: domain must be at least 2 characters long"}
    else:
        return {"message": "Valid email address"}

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8888)