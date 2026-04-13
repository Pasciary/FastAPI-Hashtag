from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session


auth_router = APIRouter(prefix="/auth", tags=["authentication"])

def criar_token(id_usuario):
    token = f"fnkdjaskwxiszlkj{id_usuario}"
    return token

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
        senha_bytes = usuario_schema.senha.encode("utf-8")
        # senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        try:
            senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Falha ao criptografar senha. "
                    f"len(chars)={len(usuario_schema.senha)}, len(bytes_utf8)={len(senha_bytes)}. "
                    f"Erro: {str(e)}"
                ),
            )
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {'mensagem': f'Usuário cadastrado com sucesso, e-mail: {usuario_schema.email}'}



@auth_router.post("/login")
async def login(login_schema: LoginSchema, session:Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")

    else:
        acess_token = criar_token(usuario.id) 
        
        # JWT é do tipo Bearer, sendo Headers = {"Acess-Token": "Bearer {Token}"}
        return {
            "acess_token": acess_token,
            "token_type": "Bearer"
        }