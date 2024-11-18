"""setup backend database here"""

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, MappedAsDataclass
# from . import settings
from .settings import SupportDB, SupportSecurity

# create Base object to build tables
class Base(MappedAsDataclass, DeclarativeBase):
    """subclassing will be converted to dataclasses"""

app_config = {}
app_config["DB_ENGINE"] = SupportDB.ENGINE.value
app_config["DB_USERNAME"] = SupportDB.USERNAME.value
app_config["DB_PASS"] = SupportDB.PWD.value
app_config["DB_HOST"] = SupportDB.HOST.value
app_config["DB_NAME"] = SupportDB.DB_NAME.value
app_config["DB_PORT"] = SupportDB.PORT.value
app_config["ACCESS_TOKEN_EXPIRE_MINUTES"] = SupportSecurity.ACCESS_TOKEN_EXPIRE_MINUTES.value
app_config["ALGORITHMS"] = SupportSecurity.ALGORITHMS.value
app_config["SECRET_KEY"] = SupportSecurity.SECRET_KEY.value

# app_config = settings.app_config
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
engine = create_engine(url_object, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

# create db dependencies to use sesssion


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
