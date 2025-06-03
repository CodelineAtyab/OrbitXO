from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/validate-email")
def validate_email(email: str):
    if email.count("@") != 1:
        return {"status": "error", "detail": "Email must have one '@'"}
    
    parts = email.split("@")
    local, domain = parts[0], parts[1]

    if len(local) == 0:
        return {"status": "error", "detail": "Local part is empty"}

    if "." not in domain:
        return {"status": "error", "detail": "Domain must contain '.'"}

    domain_parts = domain.rsplit(".", 1)
    if len(domain_parts[1]) < 2:
        return {"status": "error", "detail": "Top-level domain too short"}
    
    return {"status": "success", "detail": "Email looks valid"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
