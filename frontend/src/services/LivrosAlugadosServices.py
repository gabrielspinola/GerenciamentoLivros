import os
import requests
from dotenv import load_dotenv
from typing import List, Optional
from requests.exceptions import RequestException

from services.TokenServices import TokenManager
from model.LivrosAlugadosModel import LivrosAlugadosModel

load_dotenv()

class LivrosAlugadosServices:
    def __init__(self, username=None, password=None):
        self.BASE_URL = os.getenv("BASE_URL_BACK")
        self.username = username
        self.password = password

    #Cria um novo registro
    def create(self, aluguel: LivrosAlugadosModel) -> Optional[LivrosAlugadosModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.post(
                    f"{self.BASE_URL}/livrosalugados",
                    json=aluguel.model_dump(mode="json"),
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return LivrosAlugadosModel.model_validate(response.json())
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except RequestException as e:
            print(f"Erro ao criar aluguel: {e}")
            return (f"Erro ao criar aluguel: {e}")
                
    #Lista todos os livros
    def listar_all(self) -> List[LivrosAlugadosModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.get(
                    f"{self.BASE_URL}/livrosalugados",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return [LivrosAlugadosModel.model_validate(aluguel) for aluguel in response.json()]
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except RequestException as e:
            print(f"Erro ao listar aluguéis: {e}")
            return []
    
    #Lista todos os livros não entregues
    def listar_all_nao_entregues(self) -> List[LivrosAlugadosModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.get(
                    f"{self.BASE_URL}/livrosalugados/nao-entregues",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return [LivrosAlugadosModel.model_validate(aluguel) for aluguel in response.json()]
        except RequestException as e:
            print(f"Erro ao listar livros não entregues: {e}")
            return []    
    
    #Lista por ID
    def consultar_id(self, id) -> Optional[LivrosAlugadosModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.get(
                    f"{self.BASE_URL}/livrosalugados/{id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return LivrosAlugadosModel.model_validate(response.json())
        except RequestException as e:
            print(f"Erro ao consultar aluguel: {e}")
            return None
        
    #Deletar por ID
    def deletar(self, id):
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.delete(
                    f"{self.BASE_URL}/livrosalugados/{id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return (f"Aluguel com ID {id} deletado com sucesso.")            
        except RequestException as e:
            print (f"Erro ao deletar livro alugado: {e}")
            return (f"Erro ao deletar livro alugado: {e}")
    
    #Atualizar por ID
    def atualizar(self, altAluguel: LivrosAlugadosModel) -> Optional[LivrosAlugadosModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.put(
                    f"{self.BASE_URL}/livrosalugados/{altAluguel.idLivrosAlugados}",
                    json=altAluguel.model_dump(mode="json"),
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return LivrosAlugadosModel.model_validate(response.json())
        except RequestException as e:
            print(f"Erro ao atualizar aluguel: {e}")
            return None
            
            