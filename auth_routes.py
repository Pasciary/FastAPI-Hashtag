from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["authentication"])

@auth_router.post("/login")
async def login():
    return {"message": "Você está na rota de login."}