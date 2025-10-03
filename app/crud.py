# importar paquetes
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta

# Libros
def crear_libro(db: Session, libro: schemas.LibroCrear):
    db_libro = models.Libro(**libro.dict())
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

def obtener_libros(db: Session):
    return db.query(models.Libro).all()

def eliminar_libro(db: Session, libro_id: int):
    libro = db.query(models.Libro).filter(models.Libro.id_libro == libro_id).first()
    if libro:
        db.delete(libro)
        db.commit()
    return libro

# reservas

def crear_reserva(db: Session, reserva: schemas.ReservacionCrear):
    fecha_actual = datetime.now()
    db_reserva = models.Reservacion(
        **reserva.dict(),
        f_reserva=fecha_actual,
        f_fin_reserva=fecha_actual + timedelta(days=7),
        renovar_reserva=0,
        estado=True
    )
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

def actualizar_reserva(db: Session, reserva_id: int, data:schemas.ReservacionActualizar):
    reserva = db.query(models.Reservacion).filter(models.Reservacion.id_reserva == reserva_id).first()
    if not reserva:
        return None
    
    if data.renovar_reserva == 1:
        fecha_actual = datetime.now()
        reserva.f_reserva = fecha_actual
        reserva.f_fin_reserva = fecha_actual + timedelta(days=7)
        
    for key, value in data.dict(exclude_unset = True).items():
        setattr(reserva, key, value)
    db.commit()
    db.refresh(reserva)
    return reserva

def eliminar_reserva(db: Session, reserva_id: int):
    reserva = db.query(models.Reservacion).filter(models.Reservacion.id_reserva == reserva_id).first()
    if reserva:
        db.delete(reserva)
        db.commit()
    return reserva
