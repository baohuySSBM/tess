from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()
user_db = {}

class User:
    def __init__(self,name,email, password):
        self.name = name
        self.email = email
        self.password = password


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


@app.post("/users")
def create_user_api(user: UserCreate):
    if user.email in user_db:
        raise HTTPException(status_code=400, detail="E-Mail existiert bereits. ")
    user_obj = User(user.name, user.email, user.password)
    user_db[user.email]= user.obj
    return{"message": f"Benutzer {user.email} wurde erstellt."}

@app.delete("/users/{email}")
def delete_user_api(email:str):
    if email not in user_db:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    del user_db[email]
    return {"message": f"Benutzer {email} wurde erfolgreich gelöscht."}