from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

config = dotenv_values(".env")

user = config["POSTGRES_USER"]
password = config["POSTGRES_PASSWORD"]
host = config["POSTGRES_HOST"]
port = config["POSTGRES_PORT"]
db_name = config["POSTGRES_DB"]

DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(DATABASE_URL,
                       pool_size=20,
                       max_overflow=10,
                       pool_timeout=30,
                       pool_recycle=1800, )
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
