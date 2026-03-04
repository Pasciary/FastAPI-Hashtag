from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["orders"])

@order_router.get("/")
async def get_orders():
    """
    Route para listar os pedidos do usuário
    """
    return {"message": "Você está na rota de pedidos."}