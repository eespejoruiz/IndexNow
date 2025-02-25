account_service = (
    gscwrapper
    .generate_auth(
        client_config="/content/drive/MyDrive/000 _ Expreso/search-console-450718-997bc7dc75d1.json",
        service_account_auth=True
    )
)
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 📌 Ruta del archivo JSON de la cuenta de servicio en Google Drive
credenciales_json = "/content/drive/MyDrive/000 _ Expreso/indexing cs.json"

# 📌 Definir el `scope` correcto para la API de Indexing
SCOPES = ["https://www.googleapis.com/auth/indexing"]

def autenticar_con_cuenta_de_servicio():
    """Autentica con una cuenta de servicio sin intervención manual."""

    creds = service_account.Credentials.from_service_account_file(
        credenciales_json,
        scopes=SCOPES
    )

    return creds

# 🔹 Ejecutar la autenticación con la cuenta de servicio
credentials = autenticar_con_cuenta_de_servicio()

# 🔹 Crear servicio para la API de Indexing con los permisos correctos
service = build("indexing", "v3", credentials=credentials)

print("✅ Autenticación exitosa con cuenta de servicio. 'service' está listo para Indexing API.")
