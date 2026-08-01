from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from models.usuario import Usuario
from repositories.UsuarioRepository import UsuarioRepository
from models.token import UserInDB
from controllers.AuthController import get_current_user

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=List[Usuario], summary="Lista todos os usuários", description="Retorna uma lista com todos os usuários cadastrados no sistema. Requer autenticação.")
async def listar_usuarios(usuario_atual: UserInDB = Depends(get_current_user)):
    return UsuarioRepository().listar_todos()

@router.get("/login/{login}", response_model=Usuario, summary="Busca um usuário por login", description="Retorna os dados de um usuário específico pelo seu login. Requer autenticação.")
async def buscar_usuario_por_login(login: str, usuario_atual: UserInDB = Depends(get_current_user)):
    usuario = UsuarioRepository().buscar_por_login(login)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return usuario

@router.get("/valida-login/{login}", response_model=bool, summary="Valida se um login já existe", description="Verifica se um login já está em uso no sistema. Retorna True se o login estiver disponível, False caso contrário.")
async def validar_login(login: str):
    return UsuarioRepository().login_existe(login)

@router.get("/ativos", response_model=List[Usuario], summary="Lista todos os usuários ativos", description="Retorna uma lista com todos os usuários ativos no sistema. Requer autenticação.")
async def listar_usuarios_ativos(usuario_atual: UserInDB = Depends(get_current_user)):
    return UsuarioRepository().get_by_AllUserAtivo()

@router.get("/{id}", response_model=Usuario, summary="Busca um usuário por ID", description="Retorna os dados de um usuário específico pelo seu ID. Requer autenticação.")
async def buscar_usuario(id: int, usuario_atual: UserInDB = Depends(get_current_user)):
    usuario = UsuarioRepository().buscar_por_id(id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return usuario

@router.get("/valida-token/{token}", response_model=bool, summary="Valida um token de confirmação de e-mail", description="Verifica se um token de confirmação de e-mail é válido. Retorna True se o token for válido, False caso contrário.")
async def validar_token(token: str):
    return UsuarioRepository().valida_token(token)

@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED, summary="Cria um novo usuário", description="Cria um novo usuário no sistema. Requer autenticação.")
async def criar_usuario(usuario: Usuario, usuario_atual: UserInDB = Depends(get_current_user)):
    novo_usuario_id = UsuarioRepository().criar(usuario)
    return UsuarioRepository().buscar_por_id(novo_usuario_id)

@router.post("/com-email", response_model=Usuario, status_code=status.HTTP_201_CREATED, summary="Cria um novo usuário e envia e-mail de confirmação", description="Cria um novo usuário no sistema e envia um e-mail de confirmação. O usuário só será ativado após a confirmação do e-mail.")
async def criar_usuario_com_email(usuario: Usuario):
    novo_usuario_id = UsuarioRepository().criar_usuario_com_email(usuario)
    if not novo_usuario_id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao criar usuário")
    return UsuarioRepository().buscar_por_id(novo_usuario_id)

@router.patch("/{id}", response_model=Usuario, summary="Atualiza um usuário existente", description="Atualiza os dados de um usuário existente no sistema. Requer autenticação.")
async def atualizar_usuario(id: int, usuario: Usuario, usuario_atual: UserInDB = Depends(get_current_user)):
    usuario_existente = UsuarioRepository().buscar_por_id(id)
    if not usuario_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    UsuarioRepository().atualizar(id, usuario)
    return UsuarioRepository().buscar_por_id(id)

@router.patch("/ativar/{login}", response_model=Usuario, summary="Ativa um usuário existente", description="Ativa um usuário existente no sistema. Requer autenticação.")
async def ativar_usuario(login: str, usuario_atual: UserInDB = Depends(get_current_user)):
    usuario_existente = UsuarioRepository().buscar_por_login(login)
    if not usuario_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    UsuarioRepository().atualizar_ativo(login)
    return UsuarioRepository().buscar_por_login(login)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Deleta um usuário", description="Deleta um usuário existente no sistema. Requer autenticação.")
async def deletar_usuario(id: int, usuario_atual: UserInDB = Depends(get_current_user)):
    usuario_existente = UsuarioRepository().buscar_por_id(id)
    if not usuario_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    UsuarioRepository().deletar(id)
    return None