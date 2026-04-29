"""Rotas de pedidos.

Define endpoints relacionados a pedidos, incluindo listagem e criação de novos
pedidos associados a um usuário.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema
from models import Pedido, Usuario

order_router = APIRouter(prefix="/order", tags=["orders"], dependencies=[Depends(verificar_token)])

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



@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido:int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if not usuario.admin or usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    
    pedido.status = "CANCELADO"
    session.commit()
    return{
        "mensagem": f"Pedido numero:{pedido.id} cancelado com suscesso",
        "pedido": pedido
    }