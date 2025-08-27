# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

from models import TipoTransacao

# --- Schemas para Transação ---

class TransacaoBase(BaseModel):
    tipo: TipoTransacao
    valor: float = Field(..., gt=0, description="O valor da transação deve ser positivo.")

class TransacaoCreate(TransacaoBase):
    pass

class Transacao(TransacaoBase):
    id: int
    conta_id: int
    data_transacao: datetime

    class Config:
        from_attributes = True

# --- Schemas para Conta ---

class ContaBase(BaseModel):
    nome_titular: str = Field(..., min_length=3, description="Nome do titular da conta.")

class ContaCreate(ContaBase):
    pass

class ContaUpdate(BaseModel):
    nome_titular: str = Field(..., min_length=3, description="Novo nome do titular da conta.")

class Conta(ContaBase):
    id: int
    saldo: float
    data_criacao: datetime
    transacoes: List[Transacao] = []

    class Config:
        from_attributes = True

# --- Schemas para operações específicas ---

class DepositoSaqueRequest(BaseModel):
    valor: float = Field(..., gt=0, description="O valor para depósito ou saque deve ser positivo.")