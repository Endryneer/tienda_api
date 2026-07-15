#database

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError("Falta DATABASE_URL en las variables de entorno")

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

else:
    connect_args = {}    



engine = create_engine(DATABASE_URL, connect_args = connect_args)

# connect_args es necesario solo para SQLite

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


# Función que genera una sesión por cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db        # ← entrega la sesión a quien la pida
    finally:
        db.close()      # ← la cierra cuando termina la petición