from datetime import datetime
from mysql.connector import Error
from model.SettingsModel import SettingsModel
from typing import List, Optional

class SettingsServices:
    def __init__(self, db_connection):
        self.db = db_connection

    #Cria um novo registro
    def create(self, settings: SettingsModel) -> Optional[SettingsModel]:
        try:
            sql = "INSERT INTO settings (diasLivroEmprestado) VALUES (%s)"
            self.db.cursor.execute(sql, (settings.diasLivroEmprestado,))
            self.db.connection.commit()
            return (f"Configurações criadas com sucesso.")
        except Error as e:
            self.db.connection.rollback()
            print(f"Erro ao salvar configurações: {e}")
            return (f"Erro ao salvar configurações: {e}")
    
    #Listar todas as configurações
    def listar_config(self) -> Optional[SettingsModel]:
        try:
            sql = "SELECT * FROM settings"
            self.db.cursor.execute(sql)
            result = self.db.cursor.fetchone()
            if result:
                return SettingsModel.from_row(result) 
            else:
                return None
        except Error as e:
            print(f"Erro ao listar configurações: {e}")
            return []
    
    #Atualizar configurações
    def atualizar(self, settings: SettingsModel) -> Optional[SettingsModel]:
        try:
            sql = "UPDATE settings SET diasLivroEmprestado = %s, updatedAt = NOW() WHERE idsettings = %s"
            self.db.cursor.execute(sql, (settings.diasLivroEmprestado, settings.idsettings))
            self.db.connection.commit()
            return (f"Configurações atualizadas com sucesso.")
        except Error as e:
            self.db.connection.rollback()
            print(f"Erro ao atualizar configurações: {e}")
            return (f"Erro ao atualizar configurações: {e}")