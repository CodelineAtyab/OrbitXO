from fastapi import FastAPI
import uvicorn

app = FastAPI()

validation = {}

@app.get("/validate-email")
def validate_email(email: str):
    validation["is_valid"] = False
    if email.count("@") != 1:
        validation["message"] = "You need to have exactly one @ in your email"
    if email.startswith("@") or email.endswith("@"):
        validation["message"] = "Email cannot start or end with @"
    else:
        local = email[:email.find("@")]
        domain = email[email.find("@")+1:]
        if "." not in domain:
            validation["message"] = "Domain must contain at least one dot"
        if domain.startswith(".") or domain.endswith("."):
            validation["message"] = "Domain cannot start or end with a dot"
        if len(domain[domain.rfind(".")+1:]) > 1:
            validation["is_valid"] = True
            validation["message"] = "Valid email"
        else:
            validation["message"] = "Domain must have at least two characters after the last dot"
    return validation
    # else:
    #     print(False)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8567)