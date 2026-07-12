from datetime import datetime , timedelta, timezone
from jose import JWTError , jwt 
from passlib.context import CryptContext
from fastapi import Depends , HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from modelos import Usuario

#configuracion
SECRET_KEY = "tu_clave_secreta_muy_larga_Y_segura"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30



pwd_context = CryptContext (schemes = ["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
#                                               ↑ ruta del login

def utcnow() -> datetime :
    return datetime.now(timezone.utc)

def hashear_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def crear_token(data: dict) -> str:
    datos = data.copy()
    expiracion = utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    datos.update({"exp": expiracion})
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credenciales_exception
    except JWTError:
        raise credenciales_exception

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise credenciales_exception
    return usuario

