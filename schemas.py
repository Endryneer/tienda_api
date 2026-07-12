#schemas


from pydantic import BaseModel

# Schema para recibir datos del frontend
class ProductoCreate(BaseModel):
    nombre: str
    precio: int
    stock: int
    categoria: str

# Schema para devolver datos al frontend (incluye el id)
class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: int
    stock: int
    categoria: str
    disponible: bool

    model_config = {'from_attributes':True}# permite convertir objetos SQLAlchemy a JSON



class UsuarioCreate(BaseModel):
    email : str 
    nombre : str 
    password : str 




class UsuarioResponse(BaseModel):
    id : int 
    email : str 
    nombre : str 
    activo : bool
    model_config = {'from_attributes':True}                                                        #class Config:           
    #                                            #metodo antiguo, subclase                             #from_atributes = True


class Token(BaseModel):
    access_token : str 
    token_type : str           