from models import db
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db) # Criando conexão
        session = Session() # Criando uma instancia de sessão

        yield session
        
    finally:
        session.close()