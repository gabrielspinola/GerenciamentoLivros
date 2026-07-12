from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from models.livro import Livro
from repositories.livro_repository import livro_repo
from controllers.auth_controller import get_current_user

router = APIRouter(prefix="/livros", tags=["Livros"])

@router.get("/", response_model=List[Livro])
async def listar_livros(user: dict = Depends(get_current_user)):
    return livro_repo.listar_todos()

@router.get("/{idlivro}", response_model=Livro)
async def buscar_livro(idlivro: int, user: dict = Depends(get_current_user)):
    livro = livro_repo.buscar_por_id(idlivro)
    if not livro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    return livro

@router.post("/", response_model=Livro, status_code=status.HTTP_201_CREATED)
async def criar_livro(livro: Livro, user: dict = Depends(get_current_user)):
    novo_id = livro_repo.criar(livro)
    return livro_repo.buscar_por_id(novo_id)

@router.put("/{idlivro}", response_model=Livro)
async def atualizar_livro(idlivro: int, livro: Livro, user: dict = Depends(get_current_user)):
    existente = livro_repo.buscar_por_id(idlivro)
    if not existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    livro_repo.atualizar(idlivro, livro)
    return livro_repo.buscar_por_id(idlivro)

@router.delete("/{idlivro}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_livro(idlivro: int, user: dict = Depends(get_current_user)):
    existente = livro_repo.buscar_por_id(idlivro)
    if not existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    livro_repo.deletar(idlivro)
    return None