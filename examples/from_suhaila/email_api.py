from fastapi import FastAPI, Request
import uvicorn
app = FastAPI()
@app.post("/validate_email")
def validate_email(email: str):
    if "@" in email and "." in email and\
        email.index("@") < email.index(".") and\
        email.index("@") > 0 and\
        email.index(".") < len(email) - 1 and\
        email.index(".") - email.index("@") > 1 and\
        email.count("@") == 1 and\
        len(email[email.rindex(".")+1:]) > 2:
        return {"message": "Valid email address"}
    else:
        return {"message": "Invalid email address"}
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8888)