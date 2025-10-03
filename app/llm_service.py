# importar paquetes
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

load_dotenv()

# obtener api key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# definir el modelo de Groq
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama-3.1-8b-instant")

# prompt para transformar lenguaje natural en intent
prompt = ChatPromptTemplate.from_template("""
Eres un asistente que interpreta instrucciones para una biblioteca.

Texto del usuario: "{texto}"

Responde ÚNICAMENTE con un JSON válido y nada más.

Formato esperado (según el intent detectado):

1. Reservar un libro:
{{
  "intent": "reservar_libro",
  "titulo": "ejemplo título",
  "autor": "ejemplo autor",
  "correo": "ejemplo@correo.com",
  "id_reserva": null,
  "libro_id": null
}}

2. Renovar una reserva:
{{
  "intent": "renovar_reserva",
  "id_reserva": 123,
  "correo": "ejemplo@correo.com",                                          
  "titulo": null,
  "autor": null,
  "libro_id": null
}}

3. Eliminar una reserva:
{{
  "intent": "eliminar_reserva",
  "id_reserva": 123,
  "correo": "ejemplo@correo.com",                                          
  "titulo": null,
  "autor": null,
  "libro_id": null
}}

4. Registrar un libro:
{{
  "intent": "registrar_libro",
  "titulo": "ejemplo título",
  "autor": "ejemplo autor",
  "id_libro": null,
  "id_reserva": null
}}

5. Listar libros:
{{
  "intent": "listar_libros",
  "titulo": null,
  "autor": null,
  "id_libro": null,
  "id_reserva": null
}}

6. Eliminar un libro:
{{
  "intent": "eliminar_libro",
  "id_libro": 123,
  "titulo": null,
  "autor": null,
  "id_reserva": null
}}

Importante:
- Usa siempre estas mismas claves.
- No inventes nuevas como "id_eliminar".
- No escribas explicaciones.
- No uses Markdown ni backticks.
- Devuelve SOLO el JSON puro.
""")

def procesar_texto_llm(texto: str):
    cadena_texto = prompt | llm
    respuesta = cadena_texto.invoke({"texto": texto})
    # debug para ver respuesta cruda
    print("LLM respondió:", respuesta.content)  

    import json

    # limpiar de posibles ```json ... ``` o espacios extra
    limpio = respuesta.content.strip()
    limpio = limpio.replace("```json", "").replace("```", "")

    try:
        return json.loads(limpio)
    except Exception as e:
        print("Error al parsear JSON:", e)
        return {"intent": "desconocido", "mensaje": limpio}
