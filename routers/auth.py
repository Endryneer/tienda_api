from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from modelos import Usuario
from schemas import UsuarioCreate, UsuarioResponse, Token
from auth import hashear_password, verificar_password, crear_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registro", response_model=UsuarioResponse)
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # verificar que el email no existe
    existe = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo = Usuario(
        email=usuario.email,
        nombre=usuario.nombre,
        hashed_password=hashear_password(usuario.password)  # hashea antes de guardar
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # buscar usuario por email
    usuario = db.query(Usuario).filter(Usuario.email == form.username).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    # verificar contraseña
    if not verificar_password(form.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    # generar token
    token = crear_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}