"""Modelos e configuração do banco de dados.

Contém a configuração do engine SQLAlchemy e os modelos ORM que representam as
entidades persistidas no banco de dados.
"""

from typing import Any


from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils import ChoiceType

#Passos para criar o banco de dados:
# 1 - Criar a conexão com o banco de dados.
# 2 - Criar a base do banco de dados.
# 3 - Criar as classes/tabelas do banco de dados.
# 4 - Criar as migrations.
# 5 - Executar as migrations.
# 6 - Criar os endpoints.
# 7 - Criar os testes.
# 8 - Criar a documentação.

# 1 - cria a conexão com o banco de dados.
db = create_engine("sqlite:///database.db")

# 2 - cria a base do banco de dados.
Base = declarative_base()

# 3 - criar as classes/tabelas do banco de dados.
class Usuario(Base):
    """Modelo ORM para usuários do sistema."""
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key= True, autoincrement= True)
    nome = Column("nome", String)
    email = Column("email", String, nullable= False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default= False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        """Inicializa um usuário.

        Args:
            nome: Nome do usuário.
            email: E-mail do usuário.
            senha: Senha (preferencialmente já criptografada ao persistir).
            ativo: Flag indicando se o usuário está ativo.
            admin: Flag indicando se o usuário possui permissões de administrador.
        """
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    """Modelo ORM para pedidos realizados por usuários."""
    __tablename__ = "pedidos"

    id = Column("id", Integer, primary_key= True, autoincrement= True)
    status = Column("status", String) #pendente, cancelado, finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    itens = relationship("ItemPedido", cascade="all, delete") # caso use o cascade, se eu deletar o pedido, vai deletar os itens que são estrangeiro.

    def __init__(self, usuario, status="pendente", preco=0.0):
        """Inicializa um pedido.

        Args:
            usuario: ID do usuário associado ao pedido.
            status: Status textual do pedido.
            preco: Preço total do pedido.
        """
        self.usuario = usuario
        self.status = status
        self.preco = preco


    def calcular_preco(self):
        #percorrer todos os itens do pedido
        #somar todos os precos de todos os itens 
        #editar no campo preco o valor final do preco do pedido

        #sem listcompreenshion
        # preco_pedido = 0
        # for item in self.itens:
        #     preco_item = item.preco_unitario * item.quantidade
        #     preco_pedido += preco_item

        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)

class ItemPedido(Base):
    """Modelo ORM para itens associados a um pedido."""
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key= True, autoincrement= True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        """Inicializa um item de pedido.

        Args:
            quantidade: Quantidade do item.
            sabor: Sabor/descrição do item.
            tamanho: Tamanho do item.
            preco_unitario: Preço unitário do item.
            pedido: ID do pedido ao qual o item pertence.
        """
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido




# executa a criação dos metadados do seu banco (cria as tabelas).
