from datetime import datetime
from mysql.connector import Error
from model.LivrosAlugadosModel import LivrosAlugadosModel
from typing import List, Optional

class LivrosAlugadosServices:
    def __init__(self, db_connection):
        self.db = db_connection
        
    #Cria um novo registro
    def create(self, aluguel: LivrosAlugadosModel) -> Optional[LivrosAlugadosModel]:
        try:
            sql = "INSERT INTO livrosalugados (idusuario, idlivro, dataAluguel, dataDevolucao, dataEntrega) VALUES (%s, %s, %s, %s, %s)"
            self.db.cursor.execute(sql, (aluguel.idusuario, aluguel.idlivro, aluguel.dataAluguel, aluguel.dataDevolucao, aluguel.dataEntrega))

            self.db.connection.commit()
            return (f"Aluguel do livro com ID {aluguel.idlivro} criado com sucesso.")
        except Error as e:
            self.db.connection.rollback()
            print(f"Erro ao salvar aluguel: {e}")
            return (f"Erro ao salvar aluguel: {e}")
        
    #Lista todos os registros
    def listar_all(self) -> List[LivrosAlugadosModel]:
        try:
            sql = """SELECT la.idLivrosAlugados, la.idusuario, usu.nome, la.idlivro, lv.titulo, la.dataAluguel, la.dataDevolucao, la.dataEntrega
                       FROM bd_sgl.livrosalugados la, bd_sgl.usuarios usu, bd_sgl.livros lv
                      WHERE la.idusuario = usu.idusuario and la.idlivro   = lv.idlivro"""
            self.db.cursor.execute(sql)
            result = self.db.cursor.fetchall()
            if result:
                return [LivrosAlugadosModel.from_row(row) for row in result]
            else:
                return None
        except Error as e:
            print(f"Erro ao listar livros alugados: {e}")
            return []
        
    #Lista por ID
    def consultar_id(self, id) -> Optional[LivrosAlugadosModel]:
        try:
            sql = """SELECT la.idLivrosAlugados, la.idusuario, usu.nome, la.idlivro, lv.titulo, la.dataAluguel, la.dataDevolucao, la.dataEntrega
                       FROM bd_sgl.livrosalugados la, bd_sgl.usuarios usu, bd_sgl.livros lv
                      WHERE la.idusuario = usu.idusuario and la.idlivro   = lv.idlivro
                        AND la.idLivrosAlugados = %s"""
                        
            self.db.cursor.execute(sql, (id,))
            result = self.db.cursor.fetchone()
            if result:
                return LivrosAlugadosModel.from_row(result)
            else:
                return None
        except Error as e:
            print(f"Erro ao consultar livro alugado: {e}")
            return []
        
    #Deletar por ID
    def deletar(self, id):
        try:
            sql = "DELETE FROM livrosalugados WHERE idLivrosAlugados = %s"
            self.db.cursor.execute(sql, (id,))
            self.db.connection.commit()
            return (f"Livro alugado com ID {id} deletado com sucesso.")
        except Error as e:
            self.db.connection.rollback()
            print (f"Erro ao deletar livro alugado: {e}")
            return (f"Erro ao deletar livro alugado: {e}")
    
    #Atualizar por ID
    def atualizar(self, altAluguel: LivrosAlugadosModel) -> Optional[LivrosAlugadosModel]:
        try:
            sql = "UPDATE livrosalugados SET "
            fields = []
            values = []
            if altAluguel.idusuario:
                fields.append("idusuario = %s")
                values.append(altAluguel.idusuario)
            if altAluguel.idlivro:
                fields.append("idlivro = %s")
                values.append(altAluguel.idlivro)
            if altAluguel.dataAluguel:
                fields.append("dataAluguel = %s")
                values.append(altAluguel.dataAluguel)
            if altAluguel.dataDevolucao:
                fields.append("dataDevolucao = %s")
                values.append(altAluguel.dataDevolucao)
            if altAluguel.dataEntrega:
                fields.append("dataEntrega = %s")
                values.append(altAluguel.dataEntrega)
            values.append(altAluguel.idLivrosAlugados)
            
            if fields:
                sql += ", ".join(fields) + " WHERE idLivrosAlugados = %s"    

            self.db.cursor.execute(sql, tuple(values))
            self.db.connection.commit()
            
            if self.db.cursor.rowcount > 0:
                return(f"Aluguel com ID {altAluguel.idLivrosAlugados} atualizado com sucesso.")
            else:
                print (f"Nenhum aluguel encontrado com ID {altAluguel.idLivrosAlugados}.")
                return (f"Nenhum aluguel encontrado com ID {altAluguel.idLivrosAlugados}.")
        except Error as e:
            self.db.connection.rollback()
            print (f"Erro ao atualizar aluguel: {e}")
            return (f"Erro ao atualizar aluguel: {e}")
            
            