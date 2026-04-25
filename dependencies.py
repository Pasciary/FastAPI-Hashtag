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
        session = Session() # Criando uma instancia de sessão

        yield session
        
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    """Obtém o usuário associado ao token informado.

    Nota: a implementação atual não decodifica o JWT; ela consulta um usuário
    fixo no banco. Mantido assim para não alterar o comportamento existente.

    Args:
        token: Token JWT recebido (não utilizado na implementação atual).
        session: Sessão do SQLAlchemy injetada via dependência.

    Returns:
        Usuario | None: Usuário encontrado (ou None).
    """
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)

        id_usuario = dic_info.get("sub") # com o get só não vai dar erro, vai trazer nada.

    except JWTError:
        raise HTTPException(status_code=401, detail='Acesso Negado, Verifique a Validade do TOKEN')

    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first
    
    if not usuario:
        raise HTTPException(status_code=401, detail='Acesso Invalido.')

    return usuario