# controllers/web_controller.py
from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated

import crud
import schemas
import models
from database import get_db

router = APIRouter(
    tags=["Web Interface"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def pagina_inicial(request: Request, db: Session = Depends(get_db)):
    contas = crud.get_contas(db)
    return templates.TemplateResponse("index.html", {"request": request, "contas": contas})

@router.get("/criar-conta", response_class=HTMLResponse)
def pagina_criar_conta(request: Request):
    return templates.TemplateResponse("criar_conta.html", {"request": request})

@router.post("/criar-conta")
def processa_criar_conta(nome_titular: Annotated[str, Form()], db: Session = Depends(get_db)):
    conta_schema = schemas.ContaCreate(nome_titular=nome_titular)
    crud.create_conta(db, conta=conta_schema)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/contas/{conta_id}", response_class=HTMLResponse)
def pagina_detalhes_conta(request: Request, conta_id: int, db: Session = Depends(get_db)):
    conta = crud.get_conta(db, conta_id=conta_id)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    error_message = request.query_params.get("error")
    
    return templates.TemplateResponse("conta.html", {
        "request": request, 
        "conta": conta,
        "error_message": error_message
    })

@router.post("/contas/{conta_id}/depositar")
def processa_deposito(conta_id: int, valor: Annotated[float, Form()], db: Session = Depends(get_db)):
    db_conta = crud.get_conta(db, conta_id=conta_id)
    if db_conta and valor > 0:
        db_conta.saldo += valor
        crud.create_transacao(db, conta_id=conta_id, tipo=models.TipoTransacao.DEPOSITO, valor=valor)
        db.commit()
    return RedirectResponse(url=f"/contas/{conta_id}", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/contas/{conta_id}/sacar")
def processa_saque(conta_id: int, valor: Annotated[float, Form()], db: Session = Depends(get_db)):
    db_conta = crud.get_conta(db, conta_id=conta_id)
    
    if not db_conta or valor <= 0 or db_conta.saldo < valor:
        error_msg = "Saldo insuficiente ou valor inválido."
        return RedirectResponse(url=f"/contas/{conta_id}?error={error_msg}", status_code=status.HTTP_303_SEE_OTHER)

    db_conta.saldo -= valor
    crud.create_transacao(db, conta_id=conta_id, tipo=models.TipoTransacao.SAQUE, valor=valor)
    db.commit()
    
    return RedirectResponse(url=f"/contas/{conta_id}", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/contas/{conta_id}/deletar")
def processa_deletar_conta(conta_id: int, db: Session = Depends(get_db)):
    """Processa a exclusão de uma conta e redireciona para a página inicial."""
    crud.delete_conta(db, conta_id=conta_id)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
