"""Rotas e utilitários de autenticação.

Define endpoints de autenticação (criação de conta, login, refresh) e funções
auxiliares para criação/verificação de tokens e validação de credenciais.
"""

from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context, ACESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["authentication"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    """Cria um JWT para o usuário.

    Args:
        id_usuario: Identificador do usuário que será colocado em `sub`.
        duracao_token: Duração do token. Por padrão, usa o tempo do access token.

    Returns:
        str: Token JWT codificado.
    """

    data_expiracao = datetime.now(timezone.utc) + duracao_token # Definição de data
    dic_info = {"sub": id_usuario, "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM) # geração do token

    return jwt_codificado

def verificar_token(token, session: Session = Depends(pegar_sessao)):
    """Obtém o usuário associado ao token informado.

    Nota: a implementação atual não decodifica o JWT; ela consulta um usuário
    fixo no banco. Mantido assim para não alterar o comportamento existente.

    Args:
        token: Token JWT recebido (não utilizado na implementação atual).
        session: Sessão do SQLAlchemy injetada via dependência.

    Returns:
        Usuario | None: Usuário encontrado (ou None).
    """
    #verificar se o token é valido.
    #extrair o id do usuario valido.
    usuario = session.query(Usuario).filter(Usuario.id==1).first
    return usuario


def autenticar_usuario(email, senha, session):
    """Valida credenciais e retorna o usuário correspondente.

    Args:
        email: E-mail do usuário.
        senha: Senha em texto puro enviada no login.
        session: Sessão do SQLAlchemy.

    Returns:
        Usuario | None: Usuário autenticado, ou None se não encontrado/credenciais inválidas.
    """
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return None
    if not bcrypt_context.verify(senha, usuario.senha):
        return None

    return usuario


@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"message": "Você está na rota padrão de autenticação.", "Autenticado": False}   


@auth_router.post("/criar-conta")
async def criar_conta(usuario_schema:UsuarioSchema, session:Session = Depends(pegar_sessao)):
    """Cria um novo usuário caso o e-mail ainda não esteja cadastrado.

    Args:
        usuario_schema: Dados do usuário a ser criado.
        session: Sessão do SQLAlchemy injetada via dependência.

    Raises:
        HTTPException: Se o e-mail já estiver cadastrado ou se a senha não puder ser criptografada.

    Returns:
        dict: Mensagem de sucesso com o e-mail cadastrado.
    """
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
    """Autentica o usuário e retorna tokens de acesso e refresh.
    Args:
        login_schema: Credenciais de login (e-mail e senha).
        session: Sessão do SQLAlchemy injetada via dependência.

    Raises:
        HTTPException: Se o usuário não for encontrado ou as credenciais forem inválidas.

    Returns:
        dict: `acess_token`, `refresh_token` e `token_type`.
    """
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais invalidas.")

    else:
        acess_token = criar_token(usuario.id) 
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=REFRESH_TOKEN_EXPIRE_MINUTES)) 
        # JWT é do tipo Bearer, sendo Headers = {"Acess-Token": "Bearer {Token}"}
        return {
            "acess_token": acess_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }



@auth_router.get("/refresh")
async def use_refresh_token(token): # Esta com erro nessa parte, pois toda hora usa o session, menos essa, ele usa indiretamente.
    """Gera um novo access token a partir de um token informado.

    Args:
        token: Token recebido para validação/refresh.

    Returns:
        dict: Novo `acess_token` e `token_type`.
    """

    usuario = verificar_token(token)

    acess_token = criar_token(usuario.id)
    return {
            "acess_token": acess_token,
            "token_type": "Bearer"
        }