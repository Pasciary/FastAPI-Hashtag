from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["authentication"])

@auth_router.post("/login")
async def login():
    """
    Route para login do usuário
    """
    return {"message": "Você está na rota de login."}   