# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Importa os nossos módulos (sem "from controllers")
import models
from database import engine
from controllers import web_controller

# Cria todas as tabelas no banco de dados (se ainda não existirem)
models.Base.metadata.create_all(bind=engine)

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="Simulação Bancária",
    description="Projeto com interface web para simular operações bancárias.",
    version="1.0.0"
)

# Monta o diretório 'static' para que o navegador possa aceder ao nosso ficheiro CSS.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclui todas as rotas (endpoints) que definimos no nosso web_controller.
app.include_router(web_controller.router)

@app.get("/health", tags=["Status"])
def health_check():
    """Um endpoint simples para verificar se a aplicação está a funcionar."""
    return {"status": "ok"}
