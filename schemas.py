# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

# Importa o Enum do nosso ficheiro models.py
from models import TipoTransacao

# --- Schemas para Transação ---

# Schema base para uma transação. Contém os campos comuns.
class TransacaoBase(BaseModel):
    tipo: TipoTransacao
    valor: float = Field(..., gt=0, description="O valor da transação deve ser positivo.")

# Schema para a criação de uma transação (não será exposto diretamente na API).
class TransacaoCreate(TransacaoBase):
    pass

# Schema para exibir uma transação na resposta da API.
# Herda de TransacaoBase e adiciona os campos que vêm do banco de dados.
class Transacao(TransacaoBase):
    id: int
    conta_id: int
    data_transacao: datetime

    class Config:
        # Permite que o Pydantic leia os dados diretamente de um modelo ORM (SQLAlchemy).
        from_attributes = True

# --- Schemas para Conta ---

# Schema base para uma conta.
class ContaBase(BaseModel):
    nome_titular: str = Field(..., min_length=3, description="Nome do titular da conta.")

# Schema usado para criar uma nova conta.
class ContaCreate(ContaBase):
    pass

# Schema completo para exibir os detalhes de uma conta.
# Inclui uma lista de transações associadas.
class Conta(ContaBase):
    id: int
    saldo: float
    data_criacao: datetime
    transacoes: List[Transacao] = []

    class Config:
        from_attributes = True

# --- Schemas para operações específicas ---

# Schema para o corpo da requisição de depósito e saque.
# Garante que o valor enviado seja um número positivo.
class DepositoSaqueRequest(BaseModel):
    valor: float = Field(..., gt=0, description="O valor para depósito ou saque deve ser positivo.")
