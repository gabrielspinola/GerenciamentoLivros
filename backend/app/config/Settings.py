import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    mail_default_sender: str
    mail_server: str
    mail_port: int
    mail_use_tls: bool

    def __init__(self):
        self.db_host = os.getenv("DB_HOST")
        self.db_port = int(os.getenv("DB_PORT"))
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        self.mail_default_sender = os.getenv("MAIL_DEFAULT_SENDER")
        self.mail_server = os.getenv("MAIL_SERVER")
        self.mail_port = int(os.getenv("MAIL_PORT"))
        self.mail_use_tls = os.getenv("MAIL_USE_TLS").lower() == "true"