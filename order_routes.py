"""Rotas de pedidos.

Define endpoints relacionados a pedidos, incluindo listagem e criação de novos
pedidos associados a um usuário.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import ItemPedido, Pedido, Usuario

order_router = APIRouter(prefix="/order", tags=["orders"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def get_orders():
    """
    Route para listar os pedidos do usuário
    """
    return {"message": "Você está na rota de pedidos."}


@order_router.post("/pedido") # Passa o id do pedido via body
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



@order_router.post("/pedido/cancelar/{id_pedido}") # Passa o id do pedido via path
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


@order_router.get("/listar")
async def listar_pedido(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedido": pedidos
        }


@order_router.post("/pedido/adicionar-iten/{id_pedido}")
async def adicionar_iten_pedido(id_pedido:int, item_pedido_schema:ItemPedidoSchema, session:Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).firt()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existe ou não encontrado")
    if not usuario.admin or usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")

    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)

    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()

    return{
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }


@order_router.post("/pedido/remover-iten/{id_item_pedido}")
async def remover_iten_pedido(id_item_pedido:int, item_pedido_schema:ItemPedidoSchema, session:Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    item_pedido = session.query(ItemPedido).filter(Pedido.id==id_item_pedido).firt()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()

    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item não existe ou não encontrado")
    if not usuario.admin or usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")


    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()

    return{
        "mensagem": "Item removido com sucesso",
        "identificador do pedido": pedido.id,
        "pedido": pedido
    }


# finalizar um pedido
@order_router.post("/pedido/finalizar/{id_pedido}") # Passa o id do pedido via path
async def finalizar_pedido(id_pedido:int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if not usuario.admin or usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    
    pedido.status = "FINALIZADO"
    session.commit()
    return{
        "mensagem": f"Pedido numero:{pedido.id} finalizado com suscesso",
        "pedido": pedido
    }


# visualizar 1 pedido por inteiro
@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido:int, session:Session = Depends(pegar_sessao), usuario:Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if not usuario.admin or usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")

    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

# visualizar todos os pedidos de 1 usuario
@order_router.get("/listar/pedidos-usuario")
async def listar_pedido(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
        pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
        return {
            "pedido": pedidos
        }