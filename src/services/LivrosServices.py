from datetime import datetime
from mysql.connector import Error
from model.LivroModel import LivroModel
from typing import List, Optional

class LivroServices:
    def __init__(self, db_connection):
        self.db = db_connection
    
    #Cria um novo registro
    def create(self, livro: LivroModel) -> Optional[LivroModel]:
        try:
            sql = "INSERT INTO livros (titulo, autor, ano_publicacao, genero) VALUES (%s, %s, %s, %s)"
            self.db.cursor.execute(sql, (livro.titulo, livro.autor, livro.ano_publicacao, livro.genero))

            self.db.connection.commit()
            return (f"Livro {livro.titulo} criado com sucesso.")
        except Error as e:
            self.db.connection.rollback()
            print(f"Erro ao salvar livro: {e}")
            return (f"Erro ao salvar livro: {e}")
    
    #Lista todos os registros
    def listar_all(self) -> List[LivroModel]:
        try:
            sql = "SELECT * FROM livros"
            self.db.cursor.execute(sql)
            result = self.db.cursor.fetchall()
            if result:
                return [LivroModel.from_row(row) for row in result]
            else:
                return None
        except Error as e:
            print(f"Erro ao listar livros: {e}")
            return []
    
    #Lista por ID
    def consultar_id(self, id) -> Optional[LivroModel]:
        try:
            sql = "SELECT * FROM livros WHERE idlivro = %s"
            self.db.cursor.execute(sql, (id,))
            result = self.db.cursor.fetchone()
            if result:
                return LivroModel.from_row(result)
            else:
                return None
        except Error as e:
            print(f"Erro ao consultar livro: {e}")
            return []
    
    #Deletar por ID
    def deletar(self, id):
        try:
            sql = "DELETE FROM livros WHERE idlivro = %s"
            self.db.cursor.execute(sql, (id,))
            self.db.connection.commit()
            return (f"Livro com ID {id} deletado com sucesso.")
        except Error as e:
            self.db.connection.rollback()
            print (f"Erro ao deletar livro: {e}")
            return (f"Erro ao deletar livro: {e}")
        
    #Atualiza dados na tabela
    def atualizar(self, livro: LivroModel) -> Optional[LivroModel]:
        try:
            sql = "UPDATE livros SET "
            fields = []
            values = []
            if livro.titulo:
                fields.append("titulo = %s")
                values.append(livro.titulo)
            if livro.autor:
                fields.append("autor = %s")
                values.append(livro.autor)
            if livro.ano_publicacao:
                fields.append("ano_publicacao = %s")
                values.append(livro.ano_publicacao)
            if livro.genero:
                fields.append("genero = %s")
                values.append(livro.genero)
            values.append(livro.idlivro)

            sql += ", ".join(fields) + " WHERE idlivro = %s"
            self.db.cursor.execute(sql, tuple(values))
            self.db.connection.commit()
            if self.db.cursor.rowcount > 0:
                return(f"Livro com ID {livro.idlivro} atualizado com sucesso.")
            else:
                print (f"Nenhum livro encontrado com ID {livro.idlivro}.")
                return (f"Nenhum livro encontrado com ID {livro.idlivro}.")
        except Error as e:
            self.db.connection.rollback()
            print (f"Erro ao atualizar livro: {e}")
            return (f"Erro ao atualizar livro: {e}")