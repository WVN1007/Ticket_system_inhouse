'''setup backend database here'''
from sqlmodel import create_engine,SQLModel
from sqlalchemy import URL
import psycopg
import settings

app_config = settings.app_config
DB_ENGINE = app_config["DB_ENGINE"]
DB_USERNAME = app_config["DB_USERNAME"]
DB_PASS = app_config["DB_PASS"]
DB_HOST = app_config["DB_HOST"]
DB_NAME = app_config["DB_NAME"]
DB_PORT = app_config["DB_PORT"]

url_object = URL.create(
    f"postgresql+{DB_ENGINE}",
    username=DB_USERNAME,
    password=DB_PASS,
    host=DB_HOST,
    database=DB_NAME,
    port=int(DB_PORT)
)

# check connection
while True:
    try: 
        conn = psycopg.connect(host=DB_HOST,dbname=DB_NAME,user=DB_USERNAME, password=DB_PASS,port=DB_PORT)
        print('database is ready for engine to connect')
        # create our database engine
        engine = create_engine(url_object,echo=True)
        break
    except Exception as error:
        print('database connection failed')
        print('error:', error)


SQLModel.metadata.create_all(engine)





