# importamos paquetes de sqlalchemy y database

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

# clase para tabla libros
class Libro(Base):
    __tablename__ = "libros"
    id_libro = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    autor = Column(String(255), nullable=False)
    copias = Column(Integer, default=1)
    creado = Column(DateTime(timezone=True), server_default=func.now())

    # relacion con reservas

    reservaciones = relationship("Reservacion", back_populates="libro")

    __table_args__= (UniqueConstraint('titulo', 'autor', name='libro_invalido'),)

# clase para la tabla de reservaciones
class Reservacion(Base):
    __tablename__ = "reservaciones"
    id_reserva = Column(Integer, primary_key=True, index=True)
    libro_id = Column(Integer, ForeignKey("libros.id_libro"), nullable=False)
    correo = Column(String(255), nullable=False)
    f_reserva = Column(DateTime(timezone=True), server_default=func.now())
    f_fin_reserva = Column(DateTime(timezone=True), nullable=True)
    renovar_reserva = Column(Integer, default=0)
    estado = Column(Boolean, default=True)

    libro = relationship("Libro", back_populates="reservaciones")

    __table_args__= (UniqueConstraint('libro_id', 'correo', 'estado', name='reserva_invalido'),)

