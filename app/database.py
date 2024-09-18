"""setup backend database here"""

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import (sessionmaker, DeclarativeBase, MappedAsDataclass)
import psycopg
import time
from . import settings

app_config = settings.app_config
DB_ENGINE = app_config["DB_ENGINE"]
DB_USERNAME = app_config["DB_USERNAME"]
DB_PASS = app_config["DB_PASS"]
DB_HOST = app_config["DB_HOST"]
DB_NAME = app_config["DB_NAME"]
DB_PORT = app_config["DB_PORT"]

port = int(DB_PORT)

url_object = URL.create(
    f"postgresql+{DB_ENGINE}",
    username=DB_USERNAME,
    password=DB_PASS,
    host=DB_HOST,
    database=DB_NAME,
    port=port,
)

# create engine and sessionLocal for handling database connection
engine = create_engine(url_object, echo=True)
sessionLocal = sessionmaker(bind=engine,autoflush=False)

# create Base object to build tables

class Base(MappedAsDataclass, DeclarativeBase):
    '''subclassing will be converted to dataclasses'''

