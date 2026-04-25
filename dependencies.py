"""Dependências compartilhadas do FastAPI.

Este módulo centraliza dependências usadas nas rotas, como a criação e o ciclo
de vida da sessão do banco de dados.
"""

from models import db
from sqlalchemy.orm import sessionmaker

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