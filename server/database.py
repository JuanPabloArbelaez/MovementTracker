import os
from pathlib import Path

import pg8000
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes


PG8000 = "pg8000"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =\
#      "C:/Users/juarb/MyStuff/MovementTracker/movementtracker-credential.json"
db_config_path = Path("./db_auth.txt") 
db_config = db_config_path.read_text().split(" ")
username = db_config[0]
password = db_config[1]
address = db_config[2]
port = db_config[3]
db = db_config[4]
instance_connection_name  = db_config[5]
connector = Connector()


def cloud_sql_conn() -> pg8000.dbapi.Connection:
    conn: pg8000.dbapi.Connection = connector.connect(
        instance_connection_name,
        PG8000,
        user=username,
        password=password,
        db=db,
        ip_type=IPTypes.PUBLIC
    )
    return conn


db_engine = create_engine("postgresql+pg8000://", creator=cloud_sql_conn)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
Base = declarative_base()
