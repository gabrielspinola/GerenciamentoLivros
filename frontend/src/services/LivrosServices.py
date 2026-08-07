import os
import requests
from dotenv import load_dotenv 
from typing import List, Optional
from requests.exceptions import RequestException

from services.TokenServices import TokenManager
from model.LivroModel import LivroModel

load_dotenv()

class LivroServices:
    def __init__(self, username=None, password=None):
        self.BASE_URL = os.getenv("BASE_URL_BACK")        
        self.username = username
        self.password = password
    
    #Cria um novo registro
    def create(self, livro: LivroModel) -> Optional[LivroModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.post(
                    f"{self.BASE_URL}/livros",
                    json=livro.model_dump(mode="json"),
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return LivroModel.model_validate(response.json())
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except RequestException as e:
            print(f"Erro ao criar livro: {e}")
            return (f"Erro ao criar livro: {e}")
            
    #Lista todos os registros
    def listar_all(self) -> List[LivroModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.get(
                    f"{self.BASE_URL}/livros",
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return [LivroModel.model_validate(livro) for livro in response.json()]
            else:
                print("Não foi possível obter uma autenticação.")
                return []
        except RequestException as e:
            print(f"Erro ao listar livros: {e}")
            return []
                
    #Lista por ID
    def consultar_id(self, id) -> Optional[LivroModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.get(
                    f"{self.BASE_URL}/livros/{id}",
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return LivroModel.model_validate(response.json())
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except RequestException as e:
            print(f"Erro ao consultar livro: {e}")
            return None
    
    #Listar livros disponíveis para aluguel
    def listar_livros_disponiveis(self) -> List[LivroModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.get(
                    f"{self.BASE_URL}/livros/disponiveis",
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return [LivroModel.model_validate(livro) for livro in response.json()]
            else:
                print("Não foi possível obter uma autenticação.")
                return []
        except RequestException as e:
            print(f"Erro ao listar livros disponíveis: {e}")
            return []
        
    #Deletar por ID
    def deletar(self, id):
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.delete(
                    f"{self.BASE_URL}/livros/{id}",
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return (f"Livro com ID {id} deletado com sucesso.")
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except RequestException as e:
            print(f"Erro ao deletar livro: {e}")
            return (f"Erro ao deletar livro: {e}")

    #Bloquear por ID
    def BloqueiaLivroID(self, id):
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.patch(
                    f"{self.BASE_URL}/livros/{id}/bloquear",
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return (f"Livro com ID {id} bloqueado com sucesso.")
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except RequestException as e:
            print(f"Erro ao bloquear livro: {e}")
            return (f"Erro ao bloquear livro: {e}")

    #Desbloquear por ID
    def DesbloqueiaLivroID(self, id):
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.patch(
                    f"{self.BASE_URL}/livros/{id}/desbloquear",
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return (f"Livro com ID {id} desbloqueado com sucesso.")
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except RequestException as e:
            print(f"Erro ao desbloquear livro: {e}")
            return (f"Erro ao desbloquear livro: {e}")
        
    
    #Atualiza dados na tabela
    def atualizar(self, livro: LivroModel) -> Optional[LivroModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.put(
                    f"{self.BASE_URL}/livros/{id}",
                    json=livro.model_dump(mode="json"),
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return LivroModel.model_validate(response.json())
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except RequestException as e:
            self.db.connection.rollback()
            print (f"Erro ao atualizar livro: {e}")
            return (f"Erro ao atualizar livro: {e}")