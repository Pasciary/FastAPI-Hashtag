"""Dependências compartilhadas do FastAPI.

Este módulo centraliza dependências usadas nas rotas, como a criação e o ciclo
de vida da sessão do banco de dados.
"""

from fastapi import Depends, HTTPException
from main import ALGORITHM, SECRET_KEY, oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from jose import jwt, JWTError


def pegar_sessao():
    """Fornece uma sessão do SQLAlchemy para injeção via `Depends`.

    Yields:
        Session: Sessão ativa vinculada ao engine configurado em `models.db`.
    """
    try:
        Session = sessionmaker(bind=db) # Criando conexão
        session = Session()  # Criando uma instância de sessão

        yield session
        
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    """Obtém o usuário associado ao JWT Bearer enviado no header Authorization.

    Args:
        token: JWT (sem o prefixo "Bearer ").
        session: Sessão do SQLAlchemy injetada via dependência.

    Returns:
        Usuario | None: Usuário encontrado (ou None).
    """
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id_usuario = int(dic_info["sub"])

    except (JWTError, KeyError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail='Acesso Negado, Verifique a Validade do TOKEN')

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=401, detail='Acesso inválido.')

    return usuario