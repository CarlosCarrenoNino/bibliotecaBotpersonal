def procesar_texto_mock(texto: str):
    """
    Simulación de procesamiento LLM:
    Recibe lenguaje natural y devuelve un intent fijo en JSON.
    """

    texto = texto.lower()

    if "reservar" in texto and "libro" in texto:
        return {"intent": "reservar_libro", "libro": "Cien años de soledad"}
    elif "listar" in texto or "mostrar" in texto:
        return {"intent": "listar_libros"}
    elif "eliminar" in texto and "reserva" in texto:
        return {"intent": "eliminar_reserva", "id_reserva": 1}
    else:
        return {"intent": "desconocido", "mensaje": "No entendí la solicitud"}
    
