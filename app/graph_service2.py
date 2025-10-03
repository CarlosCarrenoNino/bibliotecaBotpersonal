import requests
import msal
import os
from datetime import datetime, timedelta

# Variables de entorno
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BUZON = os.getenv("BUZON_CORREO")

# Configuración de Graph
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

# Autenticación con MSAL
def obtener_token_msal():
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    )

    token_resultado = app.acquire_token_silent(SCOPE, account=None)

    if not token_resultado:
        token_resultado = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" not in token_resultado:
        raise Exception(f"Error obteniendo token: {token_resultado}")

    return token_resultado["access_token"]

# Leer correos del buzón
def leer_correos(top: int = 5):
    """
    Lee los últimos correos de la bandeja del buzón fijo.
    Retorna una lista con subject, from y bodyPreview.
    """
    token = obtener_token_msal()
    headers = {"Authorization": f"Bearer {token}"}

    url = f"{GRAPH_API_ENDPOINT}/users/{BUZON}/messages?$top={top}&$select=subject,from,bodyPreview,receivedDateTime"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        raise Exception(f"Error al leer correos: {response.status_code} - {response.text}")

# Enviar correo desde buzón
def enviar_correo(destinatario: str, asunto: str, contenido: str):
    """
    Envía un correo desde el buzón fijo hacia el destinatario indicado.
    """
    token = obtener_token_msal()
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

    url = f"{GRAPH_API_ENDPOINT}/users/{BUZON}/sendMail"
    response = requests.post(url, headers=headers, json=email_msg)

    if response.status_code in [200, 202]:
        return {"status": "Correo enviado correctamente"}
    else:
        raise Exception(f"Error al enviar correo: {response.status_code} - {response.text}")
