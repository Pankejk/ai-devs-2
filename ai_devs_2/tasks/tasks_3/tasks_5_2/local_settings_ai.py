from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

db_name = "ai"
user = "postgres"
host = "127.0.0.1"  # "postgres"
port = 5432
SQL_ALCHEMY_ENGINE = create_engine(f"postgresql://{user}@{host}/{db_name}")

SQL_ALCHEMY_BASE = declarative_base()
