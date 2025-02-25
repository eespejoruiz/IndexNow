import time
import os

# 📌 Ruta del archivo donde están las URLs a indexar
ruta_urls = "/content/drive/MyDrive/000 _ Expreso/urls_por_indexar.txt"
ruta_errores = "/content/drive/MyDrive/000 _ Expreso/urls_fallidas.txt"

def leer_urls(ruta):
    """Lee las URLs desde un archivo y las devuelve como una lista."""
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

def enviar_url_para_indexacion(url):
    """Envía una URL a la API de Indexing de Google y muestra el estado del envío."""
    request_body = {
        "url": url,
        "type": "URL_UPDATED"
    }

    try:
        response = service.urlNotifications().publish(body=request_body).execute()

        # 📌 Verificar si la API respondió correctamente
        if "urlNotificationMetadata" in response:
            print(f"✅ URL enviada con éxito: {url}")
            print(f"🔹 Última actualización: {response['urlNotificationMetadata'].get('latestUpdate', 'No disponible')}\n")
        else:
            print(f"⚠️ URL enviada pero sin confirmación clara: {url}")
            print(f"🔹 Respuesta: {response}\n")

        return True  # Indica que la URL se envió correctamente

    except Exception as e:
        print(f"❌ Error al enviar {url}: {e}\n")
        return False  # Indica que hubo un error

def guardar_urls_fallidas(urls):
    """Guarda las URLs que no pudieron enviarse para reintentos futuros."""
    if urls:
        with open(ruta_errores, "w") as f:
            for url in urls:
                f.write(url + "\n")
        print(f"⚠️ {len(urls)} URLs con error guardadas en '{ruta_errores}'.")

# 🔹 Leer las URLs desde el archivo
urls_a_indexar = leer_urls(ruta_urls)

if not urls_a_indexar:
    print("⚠️ No hay URLs en el archivo para indexar.")
else:
    print(f"🚀 Enviando {len(urls_a_indexar)} URLs a Google Indexing API...")

    # 🔹 Lista de URLs que fallaron al enviarse
    urls_fallidas = []

    # 🔹 Enviar todas las URLs a Google Indexing API
    for url in urls_a_indexar:
        if not enviar_url_para_indexacion(url):
            urls_fallidas.append(url)

        time.sleep(2)  # 🔹 Pausa para evitar bloqueos

    # 🔹 Guardar las URLs con errores para reintento
    guardar_urls_fallidas(urls_fallidas)

    print("✅ Proceso de envío completado.")
