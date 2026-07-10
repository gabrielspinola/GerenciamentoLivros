import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações gerais da aplicação."""

    # Chave secreta usada para assinar os tokens JWT.
    # Em produção, defina isso via variável de ambiente!
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "troque-esta-chave-em-producao")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # Swagger
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGGER = False
    
    DB_HOST=os.getenv('DB_HOST')
    DB_USER=os.getenv('DB_USER')
    DB_PASSWORD=os.getenv('DB_PASSWORD')
    DB_DATABASE=os.getenv('DB_DATABASE')
    
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_SERVER=os.getenv('MAIL_SERVER')
    MAIL_PORT=int(os.getenv('MAIL_PORT'))

    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS').lower() == 'true'
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    
    SECRET_KEY=os.getenv('SECRET_KEY')
    REFRESH_SECRET_KEY=os.getenv('REFRESH_SECRET_KEY')
    ACCESS_TOKEN_EXPIRES=int(os.getenv('ACCESS_TOKEN_EXPIRES'))
    REFRESH_TOKEN_EXPIRES=int(os.getenv('REFRESH_TOKEN_EXPIRES'))
