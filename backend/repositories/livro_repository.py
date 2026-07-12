from typing import List, Optional
from models.livro import Livro
from database.connection import get_db_connection

class LivroRepository:
    def listar_todos(self) -> List[Livro]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM livros")
                rows = cursor.fetchall()
                return [Livro(**row) for row in rows]

    def buscar_por_id(self, idlivro: int) -> Optional[Livro]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM livros WHERE idlivro = %s", (idlivro,))
                row = cursor.fetchone()
                return Livro(**row) if row else None

    def criar(self, livro: Livro) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """INSERT INTO livros (titulo, autor, ano_publicacao, genero, bloqueado)
                         VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (livro.titulo, livro.autor, livro.ano_publicacao,
                                     livro.genero, livro.bloqueado))
                return cursor.lastrowid

    def atualizar(self, idlivro: int, livro: Livro) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """UPDATE livros SET titulo=%s, autor=%s, ano_publicacao=%s,
                         genero=%s, bloqueado=%s WHERE idlivro=%s"""
                affected = cursor.execute(sql, (livro.titulo, livro.autor, livro.ano_publicacao,
                                               livro.genero, livro.bloqueado, idlivro))
                return affected > 0

    def deletar(self, idlivro: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                affected = cursor.execute("DELETE FROM livros WHERE idlivro = %s", (idlivro,))
                return affected > 0

livro_repo = LivroRepository()