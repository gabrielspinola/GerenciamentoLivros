import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from flask import current_app

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.host = current_app.config.get('DB_HOST')
        self.user = current_app.config.get('DB_USER')
        self.password = current_app.config.get('DB_PASSWORD')
        self.database = current_app.config.get('DB_DATABASE')
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Conexão com o banco de dados estabelecida com sucesso.")
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Conexão com o banco de dados encerrada.")