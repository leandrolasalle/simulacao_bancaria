# models.py
import enum
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Importa a Base do nosso ficheiro database.py (sem o ponto)
from database import Base

# Enum para definir os tipos de transação permitidos.
class TipoTransacao(str, enum.Enum):
    DEPOSITO = "deposito"
    SAQUE = "saque"

# Modelo da tabela 'contas'.
class Conta(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    nome_titular = Column(String, index=True)
    saldo = Column(Float, default=0.0)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    # Define o relacionamento com a tabela de transações.
    # Uma conta pode ter várias transações.
    transacoes = relationship("Transacao", back_populates="conta")

# Modelo da tabela 'transacoes'.
class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    conta_id = Column(Integer, ForeignKey("contas.id"))
    tipo = Column(Enum(TipoTransacao))
    valor = Column(Float)
    data_transacao = Column(DateTime(timezone=True), server_default=func.now())

    # Define o relacionamento inverso com a tabela de contas.
    conta = relationship("Conta", back_populates="transacoes")
