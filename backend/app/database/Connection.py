import pymysql
from config.Settings import Settings

def get_db_connection():
    config = Settings()
    return pymysql.connect(
        host=config.db_host,
        port=config.db_port,
        user=config.db_user,
        password=config.db_password,
        database=config.db_name,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )