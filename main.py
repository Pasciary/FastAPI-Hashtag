from typing_extensions import deprecated
from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI() 

# bcrypt puro tem limite de 72 bytes e pode dar problemas dependendo da combinação de libs.
# bcrypt_sha256 pré-hasha a senha e evita esse limite, mantendo suporte a "bcrypt" antigo.
bcrypt_context = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], deprecated="auto")

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)