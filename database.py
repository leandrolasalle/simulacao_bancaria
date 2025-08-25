# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexão com o PostgreSQL.
# Formato: "postgresql://<utilizador>:<senha>@<host>:<porta>/<nome_do_banco>"
#
# ATENÇÃO: Substitua 'sua_senha_aqui' pela senha correta que você criou.
# O erro anterior foi causado por um erro de digitação nesta linha.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Leanst1987@localhost:5432/banco_fastapi"

# Cria o motor de conexão com o banco de dados.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma fábrica de sessões (SessionLocal) que será usada para criar sessões individuais.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe Base que será herdada pelos nossos modelos ORM.
Base = declarative_base()

# Função de dependência para obter a sessão do banco de dados em cada pedido.
# Isto garante que a sessão seja sempre fechada após o pedido.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
