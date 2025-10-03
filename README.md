Prueba técnica Innovati Software
Enunciado del problema a resolver
Desarrollar una solución que permita a los usuarios gestionar las reservas de libros de una biblioteca por medio del correo electrónico.
La solución debe soportar las siguientes transacciones:
Reservar un libro
Renovar una reserva existente de un libro
Eliminar una reserva
Registrar un nuevo libro
Obtener una lista de todos los libros registrados
Eliminar un libro
La solución debe ser capaz de procesar automáticamente todos los correos que lleguen a un buzón predeterminado, siguiendo los siguientes pasos:
Leer el correo
Comprender la solicitud del usuario, la cual estará escrita en lenguaje natural.  Para este fin se debe utilizar un modelo LLM (“Large Language Model”) de Open AI.  También podría utilizar un modelo LLM gratuito que funcione bien para entender la intención del usuario.
Convertir el requerimiento en un comando SQL
Ejecutar el comando en la base de datos. 
Obtener la respuesta y formatearla de manera que sea fácil de entender por el usuario
Enviar la respuesta adecuada con la información solicitada por medio del correo electrónico.  La respuesta debe estar redactada utilizando un lenguaje natural, amable y coloquial.  La respuesta debe comenzar describiendo cuál fue la solicitud del usuario y luego presentar el resultado de la transacción. Por ejemplo, para la transacción “Reservar un libro” el resultado de la transacción podría ser: “La reserva del libro solicitado se realizó exitosamente”, o “La reservación del libro solicitado no se pudo realizar porque el libro estaba reservado ya.”


Requisitos Técnicos
Lenguaje: Python
Frameworks/Librerías y/o herramientas:
FastAPI
LangChain
Microsoft Graph API
SQLAlchemy
Base de datos relacional (MySQL)

paso a paso ejecucion de paquetes y estructura del proyecto
ejecutar py -m pip install -r requisitos.txt 
crear entorno virtual 
py -m venv venv  
venv\Scripts\activate
py -m pip install mysql-connector-python

1.Estructura DB:

Base de datos + modelos SQLAlchemy

Crear Libros y Reservaciones.

Probar con MySQL en local.

Confirmar que se pueden crear tablas y hacer CRUD básico. con py -m app.testing_db  

2.FastAPI + CRUD endpoints

Endpoints de libros (POST/GET/DELETE).

Endpoints de reservas (POST/PUT/DELETE).

Swagger (/docs) funcionando. con uvicorn app.main:app --reload y abrir http://127.0.0.1:8000/docs

3.Integración LLM (LangChain)

Ejecutar 
pip install langchain langchain-groq
pip install msal requests

Empezar con un mock (texto → JSON fijo).

Luego conectar a OpenAI u otro LLM, (se utilizo GROQ_API).

Validar que convierte bien el lenguaje natural en “intents” o SQL.

4.Procesar correos con Graph API (Microsoft) (Quedo funcional ejecutando el endpoint manualmente desde Swagger)

pip install apscheduler

Conectar al buzón.

Leer un correo y pasarlo al paso 3.

Enviar respuesta por correo con el resultado.

5.Dockerización y despliegue en Azure (Quedo Pendiente)

Dockerfile + docker-compose para local.

Subir imagen a ACR.

Desplegar a ACI/App Service.

6.Extras (Quedo Pendiente)

Tests unitarios.

Logs.

Video YouTube
