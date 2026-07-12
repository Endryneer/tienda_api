#routers/productos

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from modelos import Producto
from schemas import ProductoCreate, ProductoResponse
from typing import List
from auth import obtener_usuario_actual
from modelos import Usuario

router = APIRouter(prefix="/productos", tags=["productos"])
#                  ↑ todas las rutas empiezan con /productos

@router.get("/", response_model=List[ProductoResponse])
def obtener_productos(db: Session = Depends(get_db)):
    #                              ↑ FastAPI inyecta la sesión automáticamente
    return db.query(Producto).all()


@router.get("/{id}", response_model=ProductoResponse)
def obtener_producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail=f"Producto {id} no encontrado")
    return producto


@router.post("/", response_model=ProductoResponse)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db), usuario_actual : Usuario = Depends(obtener_usuario_actual)): # protege el endpoint
    nuevo = Producto(**producto.model_dump())
    #                ↑ convierte el schema a diccionario y lo desempaqueta

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)  # ← actualiza el objeto con el id generado
    return nuevo


@router.put("/{id}", response_model=ProductoResponse)
def actualizar_producto(id: int, datos: ProductoCreate, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail=f"Producto {id} no encontrado")
    for campo, valor in datos.model_dump().items():
        setattr(producto, campo, valor)
    db.commit()
    db.refresh(producto)
    return producto


@router.delete("/{id}")
def borrar_producto(id: int, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    producto = db.query(Producto).filter(Producto.id == id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail=f"Producto {id} no encontrado")
    db.delete(producto)
    db.commit()
    return {"mensaje": f"Producto {id} borrado"}