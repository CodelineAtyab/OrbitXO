from fastapi import FastAPI
import re 
import uvicorn

app = FastAPI()

@app.post("/validate-email")

def validate_email(email):

  pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

  if "@" not in email:
       return {"is_valid" :False, "message": "Invalid email format. Missing @ symbol."} 

  if email.count("@")>1  :
          return {"is_valid" : False, "message": "Too many @ symbol." } 

  if "." not in email.split("@")[-1]:
           return {"is_valid" : False, "message": "Domain must include a '.'" }
             
  if not re.match(pattern, email):

    return {"is_valid" : False, "message": " Invalid email format"}
  
  tld = email.split('.')[-1]
  if len(tld) < 2:
    return {"is_valid": False, "message": "TLD must be at least 2 letters."}
          
  return {"is_valid" : True, "message": "Email address is valid"}

if __name__ == "__main__" :
     uvicorn.run(app, host="0.0.0.0", port=8888)