from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from env_config import Config

DATABASE_URL = f"postgresql://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_SERVER}/{Config.DB_HOST}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind = engine, 
    autoflush = False, 
    autocommit = False
)

Base = declarative_base()