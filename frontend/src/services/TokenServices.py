import json
import os
import jwt
import requests

from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

CACHE_FILE = "token_cache.json"

load_dotenv()

class TokenManager:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self._token: str | None = None
        self._expira_em: datetime | None = None
        self.BASE_URL = os.getenv("BASE_URL_BACK")
        self.MARGEM_SEGURANCA_SEGUNDOS = int(os.getenv("MARGEM_SEGURANCA_SEGUNDOS", "30"))
        self._carregar_do_cache()

    def obter_token(self) -> str:
        """Retorna um token válido, reaproveitando o cache quando possível."""
        if self._token_valido():
            return self._token

        self._fazer_login()
        return self._token

    def _token_valido(self) -> bool:
        if not self._token or not self._expira_em:
            return False
        agora = datetime.now(timezone.utc)
        margem = timedelta(seconds=self.MARGEM_SEGURANCA_SEGUNDOS)
        return agora < (self._expira_em - margem)

    def _fazer_login(self) -> None:
        resposta = requests.post(
            f"{self.BASE_URL}/auth/login",
            json={"login": self.login, "password": self.password},
        )
        resposta.raise_for_status()
        token = resposta.json()["access_token"]

        self._token = token
        self._expira_em = self._extrair_expiracao(token)
        self._salvar_no_cache()
        print("Novo token obtido via login.")

    @staticmethod
    def _extrair_expiracao(token: str) -> datetime:
        payload = jwt.decode(token, options={"verify_signature": False})
        return datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

    def _salvar_no_cache(self) -> None:
        with open(CACHE_FILE, "w") as f:
            json.dump(
                {
                    "access_token": self._token,
                    "expira_em": self._expira_em.isoformat(),
                },
                f,
            )

    def _carregar_do_cache(self) -> None:
        if not os.path.exists(CACHE_FILE):
            return
        try:
            with open(CACHE_FILE, "r") as f:
                dados = json.load(f)
            self._token = dados["access_token"]
            self._expira_em = datetime.fromisoformat(dados["expira_em"])
            if self._token_valido():
                print("Token reaproveitado do cache.")
        except (json.JSONDecodeError, KeyError, ValueError):
            # Cache corrompido ou em formato antigo: ignora e faz login normalmente
            self._token = None
            self._expira_em = None