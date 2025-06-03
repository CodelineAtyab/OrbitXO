from fastapi import FastAPI, Body
import uvicorn

app = FastAPI()

def validate_email(email: str):
    if not email or email[0] in ["_", "-", "@", "."]:
        return {"is_valid": False, "message": "Email should start with a letter not '_', '-', '@', or '.'"}

    if "@" not in email:
        return {"is_valid": False, "message": "Email must include the '@' symbol"}

    at_pos = email.find("@")
    dot_pos = email.rfind(".")
    underscore_pos = email.find("_")
    dash_pos = email.find("-")

    if dot_pos < at_pos + 2 or dot_pos >= len(email) - 2:
        return {"is_valid": False, "message": "Invalid domain format after '@'"}
    if underscore_pos != -1 and underscore_pos < at_pos:
        return {"is_valid": False, "message": "Underscore cannot be used before '@'"}
    if dash_pos != -1 and dash_pos < at_pos:
        return {"is_valid": False, "message": "Dash cannot be used before '@'"}
    if email.count("@") > 1:
        return {"is_valid": False, "message": "Email cannot contain multiple '@' symbols"}
    return {"is_valid": True, "message": "Email address is valid"}

@app.post("/validate-email")
def validate_email_endpoint(email: str):
    return validate_email(email)

if __name__ == "__main__":
    uvicorn.run("email_validator:app", host="localhost", port=8888, reload=True)
