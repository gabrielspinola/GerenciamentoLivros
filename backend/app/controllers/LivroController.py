from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from models.livro import Livro
from repositories.LivroRepository import livro_repo

router = APIRouter(prefix="/livros", tags=["Livros"])

@router.get("/", response_model=List[Livro])
async def listar_livros():
    return livro_repo.listar_todos()


@router.post("/", response_model=Livro, status_code=status.HTTP_201_CREATED)
async def criar_livro(livro: Livro):
    novo_id = livro_repo.criar(livro)
    return livro_repo.buscar_por_id(novo_id)