from fastapi import FastAPI
import uvicorn

application = FastAPI()

@application.post("/validate-email")
def validate_email(email: str):
    if "@" not in email:
        return {"message": "Missing '@' symbol"}
    
    at_index = email.index("@")
    last_dot = email.rfind(".")
    
    if last_dot < at_index + 2:
        return {"message": "Invalid placement of domain dot"}
    
    if last_dot >= len(email) - 2:
        return {"message": "Suffix after '.' is too short"}
    
    if email.count("@") != 1:
        return {"message": "Email must include one '@' only"}
    
    return {"message": "Email format is correct"}

if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=8888)
