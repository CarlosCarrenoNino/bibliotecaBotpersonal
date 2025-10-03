# importar paquetes
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import SessionLocal, engine
from .llm_service import procesar_texto_llm
from datetime import datetime, timedelta
from . import graph_service, models, schemas, crud
from .schemas import TextoEntrada
from apscheduler.schedulers.background import BackgroundScheduler

# Crear tabla si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Biblioteca", version="1.0.0")

# Depedencia para inyección de sesion a la DB
def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# endpoint interpretar texto
@app.post("/interpretar/")
def interpretar(data: TextoEntrada, db: Session = Depends(obtener_db)):
    try:
        intent_data = procesar_texto_llm(data.texto)
        return ejecutar_intencion(intent_data, db)
    except Exception as e:
        print("Error en interpretar:", e)
        raise HTTPException(status_code=500, detail=str(e))


# función reutilizable para ejecutar intents
def ejecutar_intencion(intent_data: dict, db: Session):
    match intent_data.get("intent"):
        case "reservar_libro":
            # Buscar si el libro ya existe
            libro = db.query(models.Libro).filter(
                func.lower(models.Libro.titulo) == intent_data.get("titulo").lower().strip(),
                func.lower(models.Libro.autor) == intent_data.get("autor").lower().strip()
            ).first()

            # Si no existe, lo creamos
            if not libro:
                nuevo_libro = schemas.LibroCrear(
                    titulo=intent_data.get("titulo"),
                    autor=intent_data.get("autor"),
                    copias=1
                )
                libro = crud.crear_libro(db, nuevo_libro)

            # Crear la reserva
            reserva = schemas.ReservacionCrear(
                libro_id=libro.id_libro,
                correo=intent_data.get("correo"),
                f_reserva=datetime.now(),
                f_fin_reserva=datetime.now() + timedelta(days=7)
            )
            crud.crear_reserva(db, reserva)
            return {"mensaje": "Reserva creada exitosamente."}

        case "registrar_libro":
            libro = schemas.LibroCrear(
                titulo=intent_data.get("titulo"),
                autor=intent_data.get("autor"),
                copias=1
            )
            crud.crear_libro(db, libro)
            return {"mensaje": "Libro registrado exitosamente."}

        case "listar_libros":
            return crud.obtener_libros(db)

        case "eliminar_libro":
            return crud.eliminar_libro(db, intent_data.get("id_libro"))

        case "eliminar_reserva":
            return crud.eliminar_reserva(db, intent_data.get("id_reserva"))

        case "renovar_reserva":
            reserva_id = intent_data.get("id_reserva")
            data_update = schemas.ReservacionActualizar(
                libro_id=intent_data.get("libro_id"),
                correo=intent_data.get("correo"),
                f_reserva=datetime.now(),
                f_fin_reserva=datetime.now() + timedelta(days=7),
                renovar_reserva=1
            )
            crud.actualizar_reserva(db, reserva_id, data_update)
            return {"mensaje": "Reserva renovada (+7 días)."}

        case _:
            return {"mensaje": "No entendí la solicitud."}


# endpoint procesar correos
@app.get("/procesar_correos")
def procesar_correos(db: Session = Depends(obtener_db)):
    """
    Lee correos de un buzón, interpreta con LLM,
    ejecuta acción en DB y responde al remitente.
    """
    correos = graph_service.leer_correos()
    resultados = []

    for correo in correos:
        remitente = correo["from"]["emailAddress"]["address"]
        asunto = correo["subject"]
        cuerpo = correo.get("bodyPreview", "")

        # 1. Interpretar texto con LLM
        intent_data = procesar_texto_llm(cuerpo)

        # 2. Ejecutar acción en DB
        resultado = ejecutar_intencion(intent_data, db)

        # 3. Responder al remitente
        # Normalizar el contenido de la respuesta
        if isinstance(resultado, dict) and "mensaje" in resultado:
            contenido_respuesta = resultado["mensaje"]
        elif isinstance(resultado, list):
            # si es lista de libros
            contenido_respuesta = "Resultados:\n" + "\n".join(
                # max 200 para no hacer correo gigante
                [str(item) for item in resultado[:200]]  
            )
        else:
            contenido_respuesta = "Solicitud procesada."

        graph_service.enviar_correo(
            destinatario=remitente,
            asunto=f"Re: {asunto}",
            contenido=contenido_respuesta
        )

        resultados.append({
            "remitente": remitente,
            "asunto": asunto,
            "intencion": intent_data,
            "respuesta": resultado
        })

    return {"procesados": resultados}

# función para scheduler (abre/cierra sesión manualmente)
def procesar_correos_job():
    db = SessionLocal()
    try:
        return procesar_correos(db)
    finally:
        db.close()

# Inicializar el scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(procesar_correos_job, "interval", minutes=3)
scheduler.start()

# endpoint libros
@app.post("/libros/", response_model=schemas.LibroResponse)
def crear_libro(libro: schemas.LibroCrear, db:Session = Depends(obtener_db)):
    return crud.crear_libro(db, libro)

@app.get("/libros/", response_model=list[schemas.LibroResponse])
def listar_libros(db: Session = Depends(obtener_db)):
    return crud.obtener_libros(db)

@app.delete("/libros/{libro_id}", response_model=schemas.LibroResponse)
def borrar_libro(libro_id: int, db: Session = Depends(obtener_db)):
    libro = crud.eliminar_libro(db, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="libro no encontrado")
    return libro

# endpoints reservas
@app.post("/reservas/", response_model=schemas.ReservacionResponse)
def crear_reserva(reserva: schemas.ReservacionCrear, db:Session = Depends(obtener_db)):
    return crud.crear_reserva(db, reserva)

@app.put("/reservas/{reserva_id}", response_model=schemas.ReservacionResponse)
def actualizar_reserva(reserva_id: int, data: schemas.ReservacionActualizar, db: Session = Depends(obtener_db)):
    reserva = crud.actualizar_reserva(db, reserva_id, data)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@app.delete("/reservas/{reserva_id}", response_model=schemas.ReservacionResponse)
def borrar_reserva(reserva_id: int, db: Session = Depends(obtener_db)):
    reserva = crud.eliminar_reserva(db, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

