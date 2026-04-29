"""Esquemas Pydantic (DTOs) da API.

Define modelos de entrada/saída usados nas rotas para validação e serialização
de dados.
"""

from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    """Schema para criação/representação de usuário via API."""
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True


class PedidoSchema(BaseModel):
    """Schema para criação de pedido via API."""
    id_usuario: int

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    """Schema para autenticação (login) via API."""
    email: str
    senha: str

    class Config:
        from_attributes = True


class ItemPedidoSchema(BaseModel):
        quantidade: int
        sabor: str
        tamanho: str
        preco_unitario: float

        class Config:
            from_attributes = True