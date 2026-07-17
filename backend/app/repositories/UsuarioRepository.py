from typing import List, Optional
from models.usuario import Usuario
from database.Connection import get_db_connection

class UsuarioRepository:
    def listar_todos(self) -> List[Usuario]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios")
                rows = cursor.fetchall()
                return [Usuario(**row) for row in rows]

    def buscar_por_id(self, idusuario: int) -> Optional[Usuario]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE idusuario = %s", (idusuario,))
                row = cursor.fetchone()
                return Usuario(**row) if row else None

    def criar(self, usuario: Usuario) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """INSERT INTO usuarios (nome, login, password, dataAniversario, ativo, email)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (usuario.nome, usuario.login, usuario.password,
                                     usuario.dataAniversario, usuario.ativo, usuario.email))
                return cursor.lastrowid

    def atualizar(self, idusuario: int, usuario: Usuario) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """UPDATE usuarios SET nome=%s, login=%s, password=%s,
                         dataAniversario=%s, ativo=%s, email=%s WHERE idusuario=%s"""
                affected = cursor.execute(sql, (usuario.nome, usuario.login, usuario.password,
                                               usuario.dataAniversario, usuario.ativo,
                                               usuario.email, idusuario))
                return affected > 0

    def deletar(self, idusuario: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                affected = cursor.execute("DELETE FROM usuarios WHERE idusuario = %s", (idusuario,))
                return affected > 0
            
    def get_by_username(self, login: str) -> Optional[Usuario]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE login = %s", (login,))
                row = cursor.fetchone()
                return Usuario(**row) if row else None