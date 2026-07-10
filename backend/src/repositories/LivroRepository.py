from mysql.connector import Error
from models.LivroModel import LivroModel
from conexao import DatabaseConnection
from typing import List, Optional

class LivroRepository:
    def __init__(self):
        self.db = DatabaseConnection()
    
    #Cria um novo registro
    def create(self, livro: LivroModel) -> Optional[LivroModel]:
        if isinstance(livro, dict):
            livro = LivroModel.from_dict(livro)

        try:
            self.db.connect()
            sql = "INSERT INTO livros (titulo, autor, ano_publicacao, genero) VALUES (%s, %s, %s, %s)"
            self.db.cursor.execute(sql, (livro.titulo, livro.autor, livro.ano_publicacao, livro.genero))

            self.db.connection.commit()
            livro.idlivro = self.db.cursor.lastrowid
            self.db.close()
            return livro
        except Error as e:
            self.db.connection.rollback()
            self.db.close()
            print(f"Erro ao salvar livro: {e}")
            return (f"Erro ao salvar livro: {e}")
    
    #Lista todos os registros
    def listar_all(self) -> List[LivroModel]:
        try:
            self.db.connect()
            sql = "SELECT * FROM livros"
            self.db.cursor.execute(sql)
            result = self.db.cursor.fetchall()
            self.db.close()
            if result:
                return [LivroModel.from_row(row) for row in result]
            else:
                return None            
        except Error as e:
            print(f"Erro ao listar livros: {e}")
            self.db.close()
            return []
    
    #Lista por ID
    def consultar_id(self, id) -> Optional[LivroModel]:
        try:
            self.db.connect()
            sql = "SELECT * FROM livros WHERE idlivro = %s"
            self.db.cursor.execute(sql, (id,))
            result = self.db.cursor.fetchall()
            self.db.close()
            if result:
                return LivroModel.from_row(result[0])
            else:
                return None
        except Error as e:
            print(f"Erro ao consultar livro: {e}")
            self.db.close()
            return None
    
    #Listar livros disponíveis para aluguel
    def listar_livros_disponiveis(self) -> List[LivroModel]:
        try:
            self.db.connect()
            sql = """SELECT * FROM livros
                     WHERE bloqueado = 'N'"""
            self.db.cursor.execute(sql)
            result = self.db.cursor.fetchall()
            self.db.close()

            if result:
                return [LivroModel.from_row(row) for row in result]
            else:
                return []
        except Error as e:
            print(f"Erro ao listar livros disponíveis: {e}")
            self.db.close()
            return []
    
    #Deletar por ID
    def deletar(self, id):
        try:
            self.db.connect()
            sql = "DELETE FROM livros WHERE idlivro = %s"
            self.db.cursor.execute(sql, (id,))
            self.db.connection.commit()
            self.db.close()
            return (f"Livro com ID {id} deletado com sucesso.")
        except Error as e:
            self.db.connection.rollback()
            print (f"Erro ao deletar livro: {e}")
            self.db.close()
            return (f"Erro ao deletar livro: {e}")
        
    #Bloquear por ID
    def BloqueiaLivroID(self, id):
        try:
            self.db.connect()
            sql = "UPDATE livros SET bloqueado = 'S' WHERE idlivro = %s"
            self.db.cursor.execute(sql, (id,))
            self.db.connection.commit()
            self.db.close()
            return (f"Livro com ID {id} bloqueado com sucesso.")
        except Error as e:
            self.db.connection.rollback()
            self.db.close()
            print (f"Erro ao bloquear livro: {e}")
            return (f"Erro ao bloquear livro: {e}")
        
    #Desbloquear por ID
    def DesbloqueiaLivroID(self, id):
        try:
            self.db.connect()
            sql = "UPDATE livros SET bloqueado = 'N' WHERE idlivro = %s"
            self.db.cursor.execute(sql, (id,))
            self.db.connection.commit()
            self.db.close()
            return (f"Livro com ID {id} desbloqueado com sucesso.")
        except Error as e:
            self.db.connection.rollback()
            self.db.close()
            print (f"Erro ao desbloquear livro: {e}")
            return (f"Erro ao desbloquear livro: {e}")

    #Atualiza dados na tabela
    def atualizar(self, livro: LivroModel) -> Optional[LivroModel]:
        try:
            self.db.connect()
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
            if livro.bloqueado:
                fields.append("bloqueado = %s")
                values.append(livro.bloqueado)
            values.append(livro.idlivro)

            sql += ", ".join(fields) + " WHERE idlivro = %s"
            self.db.cursor.execute(sql, tuple(values))
            self.db.connection.commit()
            self.db.close()
            if self.db.cursor.rowcount > 0:
                return(f"Livro com ID {livro.idlivro} atualizado com sucesso.")
            else:
                print (f"Nenhum livro encontrado com ID {livro.idlivro}.")
                return (f"Nenhum livro encontrado com ID {livro.idlivro}.")
        except Error as e:
            self.db.connection.rollback()
            self.db.close()
            print (f"Erro ao atualizar livro: {e}")
            return (f"Erro ao atualizar livro: {e}")