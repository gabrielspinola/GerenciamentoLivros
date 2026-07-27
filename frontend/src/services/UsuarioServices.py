import os
from dotenv import load_dotenv 
from typing import List, Optional
import requests
from mysql.connector import Error
from model.UsuarioModel import UsuarioModel
from services.TokenServices import TokenManager

load_dotenv()

class UsuarioServices:
    def __init__(self, username=None, password=None):
        self.BASE_URL = os.getenv("BASE_URL_BACK")        
        self.username = username
        self.password = password

    #Cria um novo registro pela tela de cadastro dentro do sistema
    def create(self, usuario: UsuarioModel) -> Optional[UsuarioModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.post(
                    f"{self.BASE_URL}/usuarios",
                    json=usuario.model_dump(mode="json"),
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return UsuarioModel.model_validate(response.json())
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except Error as e:
            print(f"Erro ao criar usuário: {e}")
            return (f"Erro ao criar usuário: {e}")
        
    #Cria um novo usuário fora da tela do sistema. Envia e-mail de confirmação para o usuário. O usuário só será ativado após a confirmação do e-mail.
    def create_com_email(self, usuario: UsuarioModel) -> Optional[UsuarioModel]:
        try:
            #token_manager = TokenManager(login=self.username, password=self.password)
            #token = token_manager.obter_token()
            
            response = requests.post(
                f"{self.BASE_URL}/usuarios/com-email",
                json=usuario.model_dump(mode="json")
            )
            response.raise_for_status()
            return UsuarioModel.model_validate(response.json())            
        except Error as e:
            print(f"Erro ao criar usuário: {e}")
            return (f"Erro ao criar usuário: {e}")


    #Lista todos os registros
    def listar_all(self) -> List[UsuarioModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.get(
                    f"{self.BASE_URL}/usuarios",
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return [UsuarioModel.model_validate(item) for item in response.json()]
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except Error as e:
            print(f"Erro ao listar usuários: {e}")
            return []
 
        
    #Lista todos os registros
    def listar_allAtivos(self) -> List[UsuarioModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.get(
                    f"{self.BASE_URL}/usuarios/ativos",
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return [UsuarioModel.model_validate(item) for item in response.json()]
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except Error as e:
            print(f"Erro ao listar usuários: {e}")
            return []       
        
    #Lista por ID
    def consultar_id(self, id) -> Optional[UsuarioModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.get(
                    f"{self.BASE_URL}/usuarios/{id}",
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return UsuarioModel.model_validate(response.json())
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except Error as e:
            print(f"Erro ao consultar usuário: {e}")
            return []
        
    #Consulta por Login
    def consultar_login(self, login, password) -> Optional[UsuarioModel]:
       try:
         token_manager = TokenManager(login=login, password=password)
         token = token_manager.obter_token()
         if token:
            response = requests.get(
                f"{self.BASE_URL}/usuarios/login/{login}",
                headers = {"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return UsuarioModel.model_validate(response.json())
         else:
            print("Não foi possível obter uma autenticação.")
            return None
       
       except Error as e:
           print(f"Erro ao consultar usuário: {e}")
           return []
       
    #Verifica se o login já existe
    def validar_login(self, login) -> Optional[bool]:   
        try:
            response = requests.get(
                f"{self.BASE_URL}/usuarios/valida-login/{login}"
            )
            response.raise_for_status()
            return response.json()  # Retorna True se o login estiver disponível, False caso contrário
        except Error as e:
            print(f"Erro ao validar login: {e}")
            return None
        
    #Deletar por ID
    def deletar_id(self, id):
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.delete(
                    f"{self.BASE_URL}/usuarios/{id}",
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return (f"Usuário com ID {id} deletado com sucesso.")
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except Error as e:
            print(f"Erro ao deletar usuário: {e}")
            return (f"Erro ao deletar usuário: {e}")        
            
    #Atualiza dados na tabela
    def atualizar(self, usuario: UsuarioModel) -> Optional[UsuarioModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.patch(
                    f"{self.BASE_URL}/usuarios/{usuario.idusuario}",
                    json=usuario.model_dump(mode="json"),
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return UsuarioModel.model_validate(response.json())
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except Error as e:
            print(f"Erro ao atualizar usuário: {e}")
            return (f"Erro ao atualizar usuário: {e}")
        
        
    def ativar_usuario(self, login) -> Optional[UsuarioModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.patch(
                    f"{self.BASE_URL}/usuarios/ativar/{login}",
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return UsuarioModel.model_validate(response.json())
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except Error as e:
            print(f"Erro ao ativar usuário: {e}")
            return (f"Erro ao ativar usuário: {e}")
        
    def valida_token(self, token) -> Optional[UsuarioModel]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/usuarios/valida-token/{token}"
            )
            response.raise_for_status()
            return response.json()  # Retorna True se o login estiver disponível, False caso contrário
        except Error as e:
            print(f"Erro ao validar token: {e}")
            return None