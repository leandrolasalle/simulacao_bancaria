# crud.py
from sqlalchemy.orm import Session

# Importa os modelos e schemas que criámos
import models
import schemas

# --- Funções CRUD para a Conta ---

def get_conta(db: Session, conta_id: int):
    """Busca uma única conta no banco de dados pelo seu ID."""
    return db.query(models.Conta).filter(models.Conta.id == conta_id).first()

def get_contas(db: Session, skip: int = 0, limit: int = 100):
    """Busca todas as contas, com opção de paginação."""
    return db.query(models.Conta).offset(skip).limit(limit).all()

def create_conta(db: Session, conta: schemas.ContaCreate):
    """Cria uma nova conta no banco de dados."""
    db_conta = models.Conta(nome_titular=conta.nome_titular, saldo=0.0)
    db.add(db_conta)
    db.commit()
    db.refresh(db_conta)
    return db_conta

def delete_conta(db: Session, conta_id: int):
    """Deleta uma conta e todas as suas transações associadas."""
    db_conta = get_conta(db, conta_id=conta_id)
    if db_conta:
        # Deleta as transações primeiro para evitar problemas de chave estrangeira
        db.query(models.Transacao).filter(models.Transacao.conta_id == conta_id).delete(synchronize_session=False)
        # Deleta a conta
        db.delete(db_conta)
        db.commit()
    return db_conta

# --- Funções CRUD para a Transação ---

def create_transacao(db: Session, conta_id: int, tipo: models.TipoTransacao, valor: float):
    """Cria um registo de transação para uma conta."""
    db_transacao = models.Transacao(conta_id=conta_id, tipo=tipo, valor=valor)
    db.add(db_transacao)
    return db_transacao
