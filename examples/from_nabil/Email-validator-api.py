import fastapi
import uvicorn
import re


characters = r"^[a-z A-Z 0-9._%+-]+@[a-z A-Z 0-9.-]+\.[a-z A-Z]{2,}$"


def if_email_is_valid(Email):
    if not "@" in Email:
        return f"{Email} missing '@'"
    
    if not "." in Email:
        return f"{Email} domain is missing"
    
    if not re.fullmatch(characters, Email):
        return f"{Email} invalid format"
    
    return f"{Email} this is a valid email"


app = fastapi.FastAPI()

@app.get("/correct-email")
def correct_email(Email: str):
    information = if_email_is_valid(Email)
    return{"info", information}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)