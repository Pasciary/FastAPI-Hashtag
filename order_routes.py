"""Rotas de pedidos.

Define endpoints relacionados a pedidos, incluindo listagem e criação de novos
pedidos associados a um usuário.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/order", tags=["orders"])

@order_router.get("/")
async def get_orders():
    """
    Route para listar os pedidos do usuário
    """
    return {"message": "Você está na rota de pedidos."}


@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    """Cria um pedido para o usuário informado.

    Args:
        pedido_schema: Dados do pedido (inclui `id_usuario`).
        session: Sessão do SQLAlchemy injetada via dependência.

    Returns:
        dict: Mensagem de sucesso com o ID do novo pedido.
    """
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}