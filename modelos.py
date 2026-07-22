#modelos 

from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Producto(Base):
    __tablename__ = "productos"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    nombre     = Column(String, nullable=False)
    precio     = Column(Integer, nullable=False)
    stock      = Column(Integer, nullable=False)
    categoria  = Column(String, nullable=False)
    disponible = Column(Boolean, default=True)
    descripcion = Column(String, nullable=True)



class Usuario(Base):
    __tablename__ = "usuarios"    
    id              = Column(Integer, primary_key= True, autoincrement= True)
    email           = Column(String, nullable= False, unique= True)
    nombre         = Column(String, nullable= False)
    hashed_password = Column(String, nullable= False)
    activo          = Column(Boolean, default= True)



    
     