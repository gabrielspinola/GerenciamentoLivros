from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from models.livro import Livro
from repositories.LivroRepository import LivroRepository
from models.token import UserInDB
from controllers.AuthController import get_current_user

router = APIRouter(prefix="/livros", tags=["Livros"])

@router.get("/", response_model=List[Livro], summary="Lista todos os livros", description="Retorna uma lista com todos os livros cadastrados no sistema. Requer autenticação.")
async def listar_livros(usuario_atual: UserInDB = Depends(get_current_user)):
    return LivroRepository().listar_todos()


@router.post("/", response_model=Livro, status_code=status.HTTP_201_CREATED, summary="Cria um novo livro", description="Cria um novo livro no sistema. Requer autenticação.")
async def criar_livro(livro: Livro, usuario_atual: UserInDB = Depends(get_current_user)):
    novo_id = LivroRepository().criar(livro)
    return LivroRepository().buscar_por_id(novo_id)