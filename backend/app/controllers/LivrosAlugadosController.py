from fastapi import APIRouter, Depends, status

from models.livrosAlugados import LivrosAlugados
from repositories.LivroAlugadoRepository import LivroAlugadoRepository
from models.token import UserInDB
from controllers.AuthController import get_current_user

router = APIRouter(prefix="/livrosalugados", tags=["LivrosAlugados"])

@router.get("/", response_model=list[LivrosAlugados], summary="Lista todos os livros alugados", description="Retorna uma lista de todos os livros alugados. Requer autenticação.")
async def listar_livros_alugados(usuario_atual: UserInDB = Depends(get_current_user)):
    return LivroAlugadoRepository().listar_todos()

@router.get("/nao-entregues", response_model=list[LivrosAlugados], summary="Lista todos os livros alugados não entregues", description="Retorna uma lista de todos os livros alugados que ainda não foram entregues. Requer autenticação.")
async def listar_livros_nao_entregues(usuario_atual: UserInDB = Depends(get_current_user)):
    return LivroAlugadoRepository().buscar_todos_nao_entregues()

@router.get("/{idLivrosAlugados}", response_model=LivrosAlugados, summary="Busca um livro alugado por ID", description="Retorna os detalhes de um livro alugado específico com base no ID fornecido. Requer autenticação.")
async def buscar_livro_por_id(idLivrosAlugados: int, usuario_atual: UserInDB = Depends(get_current_user)):
    livro_alugado = LivroAlugadoRepository().buscar_por_id(idLivrosAlugados)
    if livro_alugado is None:
        return {"error": "Livro alugado não encontrado."}
    return livro_alugado

@router.post("/", response_model=LivrosAlugados, status_code=status.HTTP_201_CREATED, summary="Cria um novo registro de livro alugado", description="Cria um novo registro de livro alugado no sistema. Requer autenticação.")
async def criar_livro_alugado(livro_alugado: LivrosAlugados, usuario_atual: UserInDB = Depends(get_current_user)):
    id_novo_aluguel = LivroAlugadoRepository().criar(livro_alugado)
    return LivroAlugadoRepository().buscar_por_id(id_novo_aluguel)

@router.put("/{idLivrosAlugados}", response_model=LivrosAlugados, summary="Atualiza um registro de livro alugado", description="Atualiza os detalhes de um livro alugado existente com base no ID fornecido. Requer autenticação.")
async def atualizar_livro_alugado(idLivrosAlugados: int, livro_alugado: LivrosAlugados, usuario_atual: UserInDB = Depends(get_current_user)):
    sucesso = LivroAlugadoRepository().atualizar(idLivrosAlugados, livro_alugado)
    return LivroAlugadoRepository().buscar_por_id(idLivrosAlugados)

@router.delete("/{idLivrosAlugados}", response_model=dict, summary="Deleta um registro de livro alugado", description="Deleta um registro de livro alugado existente com base no ID fornecido. Requer autenticação.")
async def deletar_livro_alugado(idLivrosAlugados: int, usuario_atual: UserInDB = Depends(get_current_user)):
    sucesso = LivroAlugadoRepository().deletar(idLivrosAlugados)
    if not sucesso:
        return {"error": "Falha ao deletar o livro alugado."}
    return {"message": "Livro alugado deletado com sucesso."}