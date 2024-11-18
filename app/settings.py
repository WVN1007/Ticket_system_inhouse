from enum import Enum
from dotenv import dotenv_values

app_config = dotenv_values(dotenv_path=".env")

class SupportDB(Enum):
    ENGINE =  app_config['DB_ENGINE'] or "psycopg"
    USERNAME = app_config['DB_USERNAME'] or "postgres"
    HOST = app_config['DB_HOST'] or 'localhost'
    PWD = app_config['DB_PASS'] or 'postgres'
    PORT = app_config['DB_PORT'] or '5432'
    DB_NAME = app_config['DB_NAME'] or 'postgres'

class SupportSecurity(Enum):
    SECRET_KEY = app_config['SECRET_KEY']
    ALGORITHMS = app_config['ALGORITHMS']
    ACCESS_TOKEN_EXPIRE_MINUTES = app_config['ACCESS_TOKEN_EXPIRE_MINUTES']


