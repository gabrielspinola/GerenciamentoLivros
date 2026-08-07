from typing import List, Optional
from models.livrosAlugados import LivrosAlugados
from database.Connection import get_db_connection

class LivroAlugadoRepository:
    def listar_todos(self) -> List[LivrosAlugados]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT la.idLivrosAlugados, la.idusuario, usu.nome, la.idlivro, lv.titulo, la.dataAluguel, la.dataDevolucao, la.dataEntrega
                                    FROM bd_sgl.livrosalugados la, bd_sgl.usuarios usu, bd_sgl.livros lv
                                   WHERE la.idusuario = usu.idusuario and la.idlivro   = lv.idlivro""")
                rows = cursor.fetchall()
                return [LivrosAlugados(**row) for row in rows]

    def buscar_por_id(self, idLivrosAlugados: int) -> Optional[LivrosAlugados]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT la.idLivrosAlugados, la.idusuario, usu.nome, la.idlivro, lv.titulo, la.dataAluguel, la.dataDevolucao, la.dataEntrega
                                    FROM bd_sgl.livrosalugados la, bd_sgl.usuarios usu, bd_sgl.livros lv
                                   WHERE la.idusuario = usu.idusuario and la.idlivro   = lv.idlivro
                                     AND la.idLivrosAlugados = %s""", (idLivrosAlugados,))
                row = cursor.fetchone()
                return LivrosAlugados(**row) if row else None
            
    def buscar_todos_nao_entregues(self) -> List[LivrosAlugados]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT la.idLivrosAlugados, la.idusuario, usu.nome, la.idlivro, lv.titulo, la.dataAluguel, la.dataDevolucao, la.dataEntrega
                                    FROM bd_sgl.livrosalugados la, bd_sgl.usuarios usu, bd_sgl.livros lv
                                   WHERE la.idusuario = usu.idusuario and la.idlivro   = lv.idlivro
                                     AND la.dataEntrega IS NULL""")
                rows = cursor.fetchall()
                return [LivrosAlugados(**row) for row in rows]        
    
    def criar(self, livroAlugado: LivrosAlugados) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """INSERT INTO livrosAlugados (idusuario, idlivro, dataAluguel, dataDevolucao, dataEntrega)
                         VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (livroAlugado.idusuario, livroAlugado.idlivro,
                                     livroAlugado.dataAluguel, livroAlugado.dataDevolucao,
                                     livroAlugado.dataEntrega))
                return cursor.lastrowid
    
    def atualizar(self, idLivrosAlugados: int, livroAlugado: LivrosAlugados) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """UPDATE livrosAlugados SET idusuario=%s, idlivro=%s, dataAluguel=%s,
                         dataDevolucao=%s, dataEntrega=%s WHERE idLivrosAlugados=%s"""
                affected = cursor.execute(sql, (livroAlugado.idusuario, livroAlugado.idlivro,
                                               livroAlugado.dataAluguel, livroAlugado.dataDevolucao,
                                               livroAlugado.dataEntrega, idLivrosAlugados))
                return affected > 0
    
    def deletar(self, idLivrosAlugados: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                affected = cursor.execute("DELETE FROM livrosAlugados WHERE idLivrosAlugados = %s", (idLivrosAlugados,))
                return affected > 0  