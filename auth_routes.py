from fastapi import APIRouter
from models import Usuario, db
from sqlalchemy.orm import sessionmaker


auth_router = APIRouter(prefix="/auth", tags=["authentication"])

@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"message": "Você está na rota padrão de autenticação.", "Autenticado": False}   


@auth_router.post("/criar-conta")
async def criar_conta(nome:str, email:str, senha:str):
    Session = sessionmaker(bind=db) # Criando conexão
    session = Session() # Criando uma instancia de sessão
    
    usuario = session.query(Usuario).filter(Usuario.email==email).first() # Faz busca na tabela usuário
    if usuario:
        # Já existe um usuário com esse email.
        return {'mensagem': 'Já existe um usuário com esse email'}
    else:
        novo_usuario = Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()
        return {'mensagem': 'Usuário cadastrado com sucesso'}