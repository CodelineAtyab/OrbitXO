from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/check-email")
def check_email(data: str):
   
    if data.find("@") == -1:
        return {"message": "Missing '@' symbol in email"}

   
    if data.count("@") > 1:
        return {"message": "Email must contain only one '@'"}

    
    at_index = data.index("@")
    dot_index = data.rfind(".")

    
    if dot_index - at_index <= 1:
        return {"message": "'.' must appear after '@' with at least one character in between"}

   
    if len(data) - dot_index <= 2:
        return {"message": "Domain suffix is too short"}

    return {"message": "Valid email format"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
