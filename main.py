#main

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from database import engine, Base
from routers import auth as auth_router
# Importamos el router de productos
from routers import productos

# Crea las tablas en la BD al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registra las rutas de productos
app.include_router(productos.router)
app.include_router(auth_router.router)