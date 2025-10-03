# importamos paquetes
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# texto de entrada
class TextoEntrada(BaseModel):
    texto: str

# Libros
class LibroBase(BaseModel):
    titulo: str
    autor: str
    copias: int = 1

class LibroCrear(LibroBase):
    pass

class LibroResponse(LibroBase):
    id_libro: int
    creado: datetime

    class Config:
        orm_mode= True

# reservas
class ReservacionBase(BaseModel):
    correo: str

class ReservacionCrear(ReservacionBase):
    libro_id: int

class ReservacionActualizar(BaseModel):
    libro_id: Optional[int] = None
    correo: Optional[str] = None
    f_fin_reserva: Optional[datetime] = None
    renovar_reserva: Optional[int] = None
    f_reserva: Optional[datetime] = None
    estado: Optional[bool] = None

class ReservacionResponse(ReservacionBase):
    id_reserva: int
    libro_id: int
    f_reserva: datetime
    f_fin_reserva: Optional[datetime]
    renovar_reserva: int
    estado: bool

    class Config:
        orm_mode= True