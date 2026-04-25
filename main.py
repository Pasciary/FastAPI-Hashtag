"""Aplicação FastAPI e configurações globais.

Este módulo inicializa a aplicação FastAPI, carrega variáveis de ambiente e
expõe configurações utilizadas por outros módulos (ex.: autenticação e rotas).
"""

from typing_extensions import deprecated
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

app = FastAPI() 

# bcrypt puro tem limite de 72 bytes e pode dar problemas dependendo da combinação de libs.
# bcrypt_sha256 pré-hasha a senha e evita esse limite, mantendo suporte a "bcrypt" antigo.
bcrypt_context = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login-form')

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)