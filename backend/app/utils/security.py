from datetime import datetime, timedelta, timezone
from typing import Optional
from werkzeug.security import check_password_hash
import jwt

from config.Settings import Settings

class Security:
    
    def __init__(self):
        self.settings = Settings()

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta
            or timedelta(minutes=self.settings.access_token_expire_minutes)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.settings.secret_key, algorithm=self.settings.algorithm)

    def verify_password(self, usu_login_password: str, usu_pasword: str) -> bool:
        return check_password_hash(usu_login_password, usu_pasword)

    def decode_access_token(self, token: str) -> dict:
        return jwt.decode(token, self.settings.secret_key, algorithms=[self.settings.algorithm])