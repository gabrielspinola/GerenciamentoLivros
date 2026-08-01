import os
from dotenv import load_dotenv
import requests
from requests.exceptions import RequestException
from typing import Optional

from model.SettingsModel import SettingsModel
from services.TokenServices import TokenManager

load_dotenv()

class SettingsServices:
    def __init__(self, username=None, password=None):
        self.BASE_URL = os.getenv("BASE_URL_BACK")        
        self.username = username
        self.password = password

    #Listar todas as configurações
    def listar_config(self) -> Optional[SettingsModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.get(
                    f"{self.BASE_URL}/settings",
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return SettingsModel.model_validate(response.json())
            else:
                print("Não foi possível obter uma autenticação.")
                return None            
        except RequestException as e:
            print(f"Erro ao listar configurações: {e}")
            return []
    
    #Cria um novo registro ou atualiza um existente
    def criar_atualizar(self, settings: SettingsModel) -> Optional[SettingsModel]:
        try:
            token_manager = TokenManager(login=self.username, password=self.password)
            token = token_manager.obter_token()
            if token:
                response = requests.post(
                    f"{self.BASE_URL}/settings",
                    json=settings.model_dump(mode="json"),
                    headers = {"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return SettingsModel.model_validate(response.json())
            else:
                print("Não foi possível obter uma autenticação.")
                return None
        except RequestException as e:
            print(f"Erro ao atualizar configurações: {e}")
            return (f"Erro ao atualizar configurações: {e}")