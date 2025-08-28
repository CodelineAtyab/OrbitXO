from fastapi import FastAPI
import uvicorn
import re

app = FastAPI()

@app.get('/emailValidator/{link}')

def validateEmail(link):
        if re.search(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+$", link):

            return f"Email: {link} = Valid Email!"

        else:

            return f"Email: {link} = Invalid Email!!!" 
        
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)