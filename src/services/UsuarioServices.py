from datetime import datetime
from mysql.connector import Error
from model.UsuarioModel import UsuarioModel
from typing import List, Optional


class UsuarioServices:
    def __init__(self, db_connection):
        self.db = db_connection        

    #Cria um novo registro
    def create(self, usuario: UsuarioModel) -> Optional[UsuarioModel]:
        try:
            #print(usuario)
            #print(usuario.nome, usuario.login, usuario.password, usuario.dataAniversario)
            sql = "INSERT INTO usuarios (nome, login, password, dataAniversario) VALUES (%s, %s, %s, %s)"
            self.db.cursor.execute(sql, (usuario.nome, usuario.login, usuario.password, datetime.strptime(usuario.dataAniversario, '%d/%m/%Y')))
            self.db.connection.commit()
            return (f"Usuário {usuario.nome} criado com sucesso.")
        except Error as e:
            self.db.connection.rollback()
            print(f"Erro ao salvar usuário: {e}")
            return (f"Erro ao salvar usuário: {e}")

    #Lista todos os registros
    def listar_all(self) -> List[UsuarioModel]:
        try:
            sql = "SELECT * FROM usuarios"
            self.db.cursor.execute(sql)
            result = self.db.cursor.fetchall()
            if result:
                return [UsuarioModel.from_row(row) for row in result]
            else:
                return None
        except Error as e:
            print(f"Erro ao listar usuários: {e}")
            return []
    
    #Consulta por Login
    def consultar_login(self, login) -> Optional[UsuarioModel]:
        try:
            sql = "SELECT * FROM usuarios WHERE login = %s"
            self.db.cursor.execute(sql, (login,))
            result = self.db.cursor.fetchone()
            if result:
                return UsuarioModel.from_row(result)
            else:
                return None
        except Error as e:
            print(f"Erro ao consultar usuário: {e}")
            return []

    #Deletar por ID
    def deletar_id(self, id):
        try:
            sql = "DELETE FROM usuarios WHERE idusuario = %s"
            self.db.cursor.execute(sql, (id,))
            self.db.connection.commit()
            return (f"Usuário com ID {id} deletado com sucesso.")
        except Error as e:
            self.db.connection.rollback()
            print (f"Erro ao deletar usuário: {e}")
            return (f"Erro ao deletar usuário: {e}")
            
    #Atualiza dados na tabela
    def atualizar(self, usuario: UsuarioModel) -> Optional[UsuarioModel]:
        try:
            sql = "UPDATE usuarios SET "
            fields = []
            values = []
            if usuario.nome:
                fields.append("nome = %s")
                values.append(usuario.nome)
            if usuario.login:
                fields.append("login = %s")
                values.append(usuario.login)
            if usuario.password:
                fields.append("password = %s")
                values.append(usuario.password)
            if usuario.dataAniversario:
                fields.append("dataAniversario = %s")
                values.append(usuario.dataAniversario)
            values.append(usuario.idusuario)

            sql += ", ".join(fields) + " WHERE idusuario = %s"
            self.db.cursor.execute(sql, tuple(values))
            self.db.connection.commit()
            if self.db.cursor.rowcount > 0:
                return(f"Usuário com ID {usuario.idusuario} atualizado com sucesso.")
            else:
                print (f"Nenhum usuário encontrado com ID {usuario.idusuario}.")
                return (f"Nenhum usuário encontrado com ID {usuario.idusuario}.")
        except Error as e:
            self.db.connection.rollback()
            print (f"Erro ao atualizar usuário: {e}")
            return (f"Erro ao atualizar usuário: {e}")