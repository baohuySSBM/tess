import bcrypt
import re
import smtplib
import os
import uuid
from dotenv import load_dotenv
from datetime import datetime
from email.message import EmailMessage
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional



load_dotenv()

app = FastAPI()
users_by_email = {}
DATE_FORMAT = "%d.%m.%Y %H:%M:%S"



class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: str


class User:
    def __init__(self, name, email , password):
        self.validate(name, email, password)
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password_hash = self.hash_password(password)
        self.created_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.updated_at = self.created_at

    @staticmethod
    def validate(name,email, password):
        if email in users_by_email:
            raise ValueError(f"E-Mail '{email}' ist bereits registriert.")
        if not (3 <= len(name) <= 20):
            raise ValueError("Benutzername muss zwischen 3 und 20 Zeichen lang sein.")
        if len(password) < 10 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password):
            raise ValueError("Passwort muss mindestens 10 Zeichen lang sein und Groß- sowie Kleinbuchstaben enthalten.")

def send_welcome_email(to, username):
    msg = EmailMessage()
    msg['Subject'] = 'Willkommen zu deinem neuen Account!'
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = to
    msg.set_content(f"Hallo {username}, \n\n dein Account wurde erfolgreich erstellt.\n\nViele Grüße,\nDein Team")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
            smtp.send_message(msg)
    except Exception as e:
        print(f"❌ Fehler beim Mailversand: {e}")

@app.post("/users", response_model=UserResponse)
def create_user(data: UserCreate):
    try:
        user = User(data.name, data.email, data.password)
        users_by_email[user.email] = user
        send_welcome_email(user.email, user.name)
        return UserResponse(id=user.id, name=user.name, email=user.email, created_at=user.created_at)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




