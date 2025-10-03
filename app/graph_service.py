import requests
import msal
import os
from datetime import datetime, timedelta

# Variables de entorno
CLIENT_ID = os.getenv("CLIENT_ID")
BUZON = os.getenv("BUZON_CORREO")

# Configuración para cuentas personales
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES = ["Mail.Read", "Mail.Send", "User.Read"]
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

# Token global (se guarda en memoria)
access_token = None

# Autenticación delegada con flujo de dispositivo
def obtener_token_delegado():
    global access_token
    if access_token:
        return access_token

    app = msal.PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)
    flow = app.initiate_device_flow(scopes=SCOPES)

    if "user_code" not in flow:
        raise Exception("No se pudo iniciar el flujo de dispositivo")

    print(flow["message"])  # Instrucciones para el usuario

    token_result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in token_result:
        raise Exception(f"Error obteniendo token: {token_result.get('error_description')}")

    access_token = token_result["access_token"]
    return access_token

# Leer correos del buzón
def leer_correos(top: int = 5):
    token = obtener_token_delegado()
    headers = {"Authorization": f"Bearer {token}"}

    url = f"{GRAPH_API_ENDPOINT}/me/messages?$top={top}&$select=subject,from,bodyPreview,receivedDateTime"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        raise Exception(f"Error al leer correos: {response.status_code} - {response.text}")

# Enviar correo desde buzón
def enviar_correo(destinatario: str, asunto: str, contenido: str):
    token = obtener_token_delegado()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    email_msg = {
        "message": {
            "subject": asunto,
            "body": {"contentType": "Text", "content": contenido},
            "toRecipients": [{"emailAddress": {"address": destinatario}}],
        }
    }

    url = f"{GRAPH_API_ENDPOINT}/me/sendMail"
    response = requests.post(url, headers=headers, json=email_msg)

    if response.status_code in [200, 202]:
        return {"status": "Correo enviado correctamente"}
    else:
        raise Exception(f"Error al enviar correo: {response.status_code} - {response.text}")