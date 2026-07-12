#database

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./tienda.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
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