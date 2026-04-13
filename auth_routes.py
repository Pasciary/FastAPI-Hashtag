from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session


auth_router = APIRouter(prefix="/auth", tags=["authentication"])

@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"message": "Você está na rota padrão de autenticação.", "Autenticado": False}   


@auth_router.post("/criar-conta")
async def criar_conta(usuario_schema:UsuarioSchema, session:Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first() # Faz busca na tabela usuário
    if usuario:
        # Já existe um usuário com esse email.
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {'mensagem': f'Usuário cadastrado com sucesso, e-mail: {usuario_schema.email}'}