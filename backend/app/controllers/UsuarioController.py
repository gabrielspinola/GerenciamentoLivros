from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from models.usuario import Usuario
from repositories.UsuarioRepository import UsuarioRepository
from models.token import UserInDB
from controllers.AuthController import get_current_user

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=List[Usuario], summary="Lista todos os usuários", description="Retorna uma lista com todos os usuários cadastrados no sistema. Requer autenticação.")
async def listar_usuarios(usuario_atual: UserInDB = Depends(get_current_user)):
    return UsuarioRepository.listar_todos()


@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED, summary="Cria um novo usuário", description="Cria um novo usuário no sistema. Requer autenticação.")
async def criar_usuario(usuario: Usuario, usuario_atual: UserInDB = Depends(get_current_user)):
    novo_usuario_id = UsuarioRepository.criar(usuario)
    return UsuarioRepository.buscar_por_id(novo_usuario_id)

