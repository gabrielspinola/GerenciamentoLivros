from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.models.livro import Livro
from app.repositories.livro_repository import livro_repo
from app.controllers.auth_controller import get_current_user

router = APIRouter(prefix="/livros", tags=["Livros"])

# ========== SCHEMAS ==========

class LivroCriarRequest(BaseModel):
    titulo: str
    autor: str
    ano_publicacao: int
    genero: str
    bloqueado: str

class LivroCriarResponse(BaseModel):
    idlivro: int
    titulo: str
    autor: str
    ano_publicacao: int
    genero: str
    bloqueado: str

class LivrosBatchResponse(BaseModel):
    inseridos: List[LivroCriarResponse]
    erros: List[dict]
    total_recebidos: int
    total_inseridos: int
    total_erros: int


# ========== ROTAS ==========

@router.get("/", response_model=List[Livro])
async def listar_livros(user: dict = Depends(get_current_user)):
    return livro_repo.listar_todos()


@router.get("/{idlivro}", response_model=Livro)
async def buscar_livro(idlivro: int, user: dict = Depends(get_current_user)):
    livro = livro_repo.buscar_por_id(idlivro)
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado"
        )
    return livro


@router.post("/", response_model=Livro, status_code=status.HTTP_201_CREATED)
async def criar_livro(livro: Livro, user: dict = Depends(get_current_user)):
    novo_id = livro_repo.criar(livro)
    return livro_repo.buscar_por_id(novo_id)


@router.post("/batch", response_model=LivrosBatchResponse, status_code=status.HTTP_201_CREATED)
async def criar_livros_em_lote(
    livros: List[LivroCriarRequest],
    user: dict = Depends(get_current_user)
):
    inseridos: List[LivroCriarResponse] = []
    erros: List[dict] = []

    for idx, livro_req in enumerate(livros):
        try:
            livro = Livro(
                titulo=livro_req.titulo,
                autor=livro_req.autor,
                ano_publicacao=livro_req.ano_publicacao,
                genero=livro_req.genero,
                bloqueado=livro_req.bloqueado
            )
            novo_id = livro_repo.criar(livro)
            livro_salvo = livro_repo.buscar_por_id(novo_id)
            inseridos.append(LivroCriarResponse(**livro_salvo.model_dump()))
        except Exception as e:
            erros.append({
                "indice": idx,
                "livro": livro_req.model_dump(),
                "erro": str(e)
            })

    return LivrosBatchResponse(
        inseridos=inseridos,
        erros=erros,
        total_recebidos=len(livros),
        total_inseridos=len(inseridos),
        total_erros=len(erros)
    )


@router.put("/{idlivro}", response_model=Livro)
async def atualizar_livro(
    idlivro: int,
    livro: Livro,
    user: dict = Depends(get_current_user)
):
    existente = livro_repo.buscar_por_id(idlivro)
    if not existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado"
        )
    livro_repo.atualizar(idlivro, livro)
    return livro_repo.buscar_por_id(idlivro)


@router.put("/batch", response_model=dict)
async def atualizar_livros_em_lote(
    livros: List[Livro],
    user: dict = Depends(get_current_user)
):
    atualizados = 0
    erros = []

    for idx, livro in enumerate(livros):
        try:
            if livro.idlivro is None:
                raise ValueError("idlivro é obrigatório para atualização")
            existente = livro_repo.buscar_por_id(livro.idlivro)
            if not existente:
                raise ValueError(f"Livro com idlivro={livro.idlivro} não encontrado")
            livro_repo.atualizar(livro.idlivro, livro)
            atualizados += 1
        except Exception as e:
            erros.append({"indice": idx, "erro": str(e)})

    return {
        "total_recebidos": len(livros),
        "total_atualizados": atualizados,
        "total_erros": len(erros),
        "erros": erros
    }


@router.delete("/{idlivro}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_livro(idlivro: int, user: dict = Depends(get_current_user)):
    existente = livro_repo.buscar_por_id(idlivro)
    if not existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado"
        )
    livro_repo.deletar(idlivro)
    return None


@router.delete("/batch", status_code=status.HTTP_200_OK)
async def deletar_livros_em_lote(
    ids: List[int],
    user: dict = Depends(get_current_user)
):
    deletados = 0
    nao_encontrados = []

    for idlivro in ids:
        existente = livro_repo.buscar_por_id(idlivro)
        if existente:
            livro_repo.deletar(idlivro)
            deletados += 1
        else:
            nao_encontrados.append(idlivro)

    return {
        "total_solicitados": len(ids),
        "total_deletados": deletados,
        "nao_encontrados": nao_encontrados
    }