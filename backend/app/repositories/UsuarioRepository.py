from typing import List, Optional
from models.usuario import Usuario
from database.Connection import get_db_connection
from utils.email import send_confirmation_email, verify_confirmation_token

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
    
    def buscar_por_login(self, login: str) -> Optional[Usuario]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE login = %s", (login,))
                row = cursor.fetchone()
                return Usuario(**row) if row else None
    
    def login_existe(self, login: str) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM usuarios WHERE login = %s", (login,))
                if cursor.rowcount == 0:
                    return False
                else:
                    return True

    def criar(self, usuario: Usuario, ativo: bool = True) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """INSERT INTO usuarios (nome, login, password, dataAniversario, ativo, email)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                if ativo:
                    usuario.ativo = 'A'
                else:
                    usuario.ativo = 'I'
                cursor.execute(sql, (usuario.nome, usuario.login, usuario.password,
                                     usuario.dataAniversario, usuario.ativo, usuario.email))
                return cursor.lastrowid

    def criar_usuario_com_email(self, usuario: Usuario) -> int:        
        # Aqui você pode adicionar a lógica para enviar o e-mail de confirmação
        if send_confirmation_email(usuario.email, usuario.nome, usuario.login):
            id = self.criar(usuario, ativo = False)
            return id
        return None

    def atualizar(self, idusuario: int, usuario: Usuario) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """UPDATE usuarios SET nome=%s, login=%s, password=%s,
                         dataAniversario=%s, ativo=%s, email=%s WHERE idusuario=%s"""
                affected = cursor.execute(sql, (usuario.nome, usuario.login, usuario.password,
                                               usuario.dataAniversario, usuario.ativo,
                                               usuario.email, idusuario))
                return affected > 0
    
    def atualizar_ativo(self, login: str) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """UPDATE usuarios SET ativo='A' WHERE login=%s"""
                affected = cursor.execute(sql, (login,))
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
            
    def get_by_AllUserAtivo(self) -> List[Usuario]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE ativo = 'A'")
                rows = cursor.fetchall()
                return [Usuario(**row) for row in rows]
            
    def valida_token(self, token: str) -> Optional[Usuario]:
        data = verify_confirmation_token(token)
        if not data:
            return False
        login = data.get("login")
        return self.atualizar_ativo(login)