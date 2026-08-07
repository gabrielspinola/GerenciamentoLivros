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

@router.get("/disponiveis", response_model=List[Livro], summary="Lista livros disponíveis", description="Retorna uma lista com todos os livros disponíveis (não bloqueados) no sistema. Requer autenticação.")
async def listar_livros_disponiveis(usuario_atual: UserInDB = Depends(get_current_user)):
    return LivroRepository().buscar_livros_disponiveis()

@router.get("/{id}", response_model=Livro, summary="Busca livro por ID", description="Retorna os dados de um livro específico pelo seu ID. Requer autenticação.")
async def consultar_livro(id: int, usuario_atual: UserInDB = Depends(get_current_user)):
    livro = LivroRepository().buscar_por_id(id)
    if not livro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    return livro

@router.post("/", response_model=Livro, status_code=status.HTTP_201_CREATED, summary="Cria um novo livro", description="Cria um novo livro no sistema. Requer autenticação.")
async def criar_livro(livro: Livro, usuario_atual: UserInDB = Depends(get_current_user)):
    novo_id = LivroRepository().criar(livro)
    return LivroRepository().buscar_por_id(novo_id)

@router.put("/{id}", response_model=Livro, summary="Atualiza um livro existente", description="Atualiza os dados de um livro existente no sistema. Requer autenticação.")
async def atualizar_livro(id: int, livro: Livro, usuario_atual: UserInDB = Depends(get_current_user)):
    livro_existente = LivroRepository().buscar_por_id(id)
    if not livro_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    LivroRepository().atualizar(id, livro)
    return LivroRepository().buscar_por_id(id)

@router.patch("/{id}/bloquear", response_model=Livro, summary="Bloqueia um livro", description="Bloqueia um livro existente no sistema. Requer autenticação.")
async def bloquear_livro(id: int, usuario_atual: UserInDB = Depends(get_current_user)): 
    livro_existente = LivroRepository().buscar_por_id(id)
    if not livro_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    LivroRepository().bloquearLivroId(id)
    return LivroRepository().buscar_por_id(id)

@router.patch("/{id}/desbloquear", response_model=Livro, summary="Desbloqueia um livro", description="Desbloqueia um livro existente no sistema. Requer autenticação.")
async def desbloquear_livro(id: int, usuario_atual: UserInDB = Depends(get_current_user)):
    livro_existente = LivroRepository().buscar_por_id(id)
    if not livro_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    LivroRepository().desbloquearLivroId(id)
    return LivroRepository().buscar_por_id(id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Deleta um livro", description="Deleta um livro existente no sistema. Requer autenticação.")
async def deletar_livro(id: int, usuario_atual: UserInDB = Depends(get_current_user)):
    livro_existente = LivroRepository().buscar_por_id(id)
    if not livro_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    LivroRepository().deletar(id)
    return None