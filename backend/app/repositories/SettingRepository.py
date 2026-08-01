from typing import List, Optional
from models.setting import Settings
from database.Connection import get_db_connection

class SettingRepository:
    def obter_settings(self) -> Optional[Settings]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM settings")
                row = cursor.fetchone()
                return Settings(**row) if row else None
    
    def criar(self, settings: Settings) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = "INSERT INTO settings (diasLivroEmprestado) VALUES (%s)"
                cursor.execute(sql, settings.diasLivroEmprestado)
                return cursor.lastrowid
            
    def atualizar(self, settings: Settings) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = "UPDATE settings SET diasLivroEmprestado = %s, updatedAt = NOW() WHERE idsettings = %s"
                affected = cursor.execute(sql, (settings.diasLivroEmprestado, settings.idsettings))
                return affected > 0