from app.database import Base, engine, SessionLocal
from app.models import Libro, Reservacion

# crear migracion de las tablas en la DB
print("Corriendo migracion")
Base.metadata.create_all(bind=engine)

# crear sesion 
db = SessionLocal()

# Insertar libro
libro = Libro(titulo="Cien años de soledad", autor="Gabriel García Marquez", copias=15)
db.add(libro)
db.commit()
db.refresh(libro)
print(f"Libro guardado: {libro.id_libro} - {libro.titulo}")

# seleccionar libros

libros = db.query(Libro).all()
print("Totalidad de libros :")
for li in libros:
    print(f"- {li.id_libro}: {li.titulo} ({li.autor})")

# guardar reserva
reserva = Reservacion(libro_id=libro.id_libro, correo="carlosalbertonino94@gmail.com")
db.add(reserva)
db.commit()
db.refresh(reserva)
print(f"Reserva guardada: {reserva.id_reserva} para {reserva.correo}")

# seleccionar reservas
reservas = db.query(Reservacion).all()
print(f"Total reservas:")
for re in reservas:
    print(f"- {re.id_reserva}: {re.libro_id} para el correo {re.correo}")

# Actualizar libros
libro.titulo = "Cien años de soledad (Edición revisada)"
db.commit()
print("Libro actualizado", db.query(Libro).first().titulo)

# Eliminar reserva
db.delete(reserva)
db.commit()
print("Reserva eliminada")

db.close()
