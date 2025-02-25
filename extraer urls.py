import requests
import xml.etree.ElementTree as ET
import os
import gzip
import io
import time

# 📌 URLs base
sitemap_index_url = "https://www.expreso.ec/sitemap-index.xml"
ruta_indexadas = "/content/drive/MyDrive/000 _ Expreso/urls_indexadas.txt"
ruta_por_indexar = "/content/drive/MyDrive/000 _ Expreso/urls_por_indexar.txt"

def obtener_sitemaps(url):
    """Obtiene la lista de archivos sitemap desde el sitemap index con reintentos en caso de fallo."""
    for intento in range(3):  # Reintentar hasta 3 veces
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Verificar si el contenido es XML válido
            if "xml" in response.headers.get("Content-Type", ""):
                root = ET.fromstring(response.content)
                sitemaps = [elem.text for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
                return sitemaps
            else:
                print("❌ El contenido recibido no es XML válido.")
                return []

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error al obtener el sitemap index. Intento {intento + 1}/3: {e}")
            time.sleep(2)

    print("❌ No se pudo obtener el sitemap index después de 3 intentos.")
    return []

def obtener_urls_de_sitemaps(lista_sitemaps):
    """Escanea todos los sitemaps y extrae las URLs, descomprimiendo archivos .gz si es necesario."""
    urls_totales = set()

    for sitemap in lista_sitemaps:
        for intento in range(3):  # Reintentar hasta 3 veces en caso de error
            try:
                response = requests.get(sitemap, timeout=10)
                response.raise_for_status()

                # Si el archivo es .xml.gz, descomprimirlo antes de procesarlo
                if sitemap.endswith(".gz"):
                    with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
                        xml_content = f.read().decode("utf-8")
                else:
                    xml_content = response.content.decode("utf-8")

                # Validar si el XML es válido
                if not xml_content.strip().startswith("<"):
                    print(f"⚠️ {sitemap} no contiene XML válido.")
                    continue

                # Parsear el XML
                root = ET.fromstring(xml_content)
                urls = [elem.text for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
                urls_totales.update(urls)
                break  # Salir del bucle si el intento fue exitoso

            except (requests.exceptions.RequestException, ET.ParseError) as e:
                print(f"⚠️ Error en intento {intento + 1}/3 con {sitemap}: {e}")
                time.sleep(2)  # Esperar antes de reintentar

    return urls_totales

def leer_urls_indexadas(ruta):
    """Lee las URLs ya indexadas desde el archivo."""
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            return set(f.read().splitlines())
    return set()

def guardar_urls_nuevas(ruta, urls_nuevas):
    """Guarda solo las nuevas URLs en el archivo (sobrescribe el archivo anterior)."""
    if urls_nuevas:
        with open(ruta, "w") as f:  # ⚠️ 'w' para sobrescribir el archivo anterior
            for url in urls_nuevas:
                f.write(url + "\n")
        print(f"✅ {len(urls_nuevas)} nuevas URLs guardadas en '{ruta}'.")
    else:
        print("⚠️ No hay nuevas URLs para agregar.")

def actualizar_urls_indexadas(ruta, urls_nuevas):
    """Agrega las nuevas URLs indexadas al archivo `urls_indexadas.txt`."""
    if urls_nuevas:
        with open(ruta, "a") as f:  # ⚠️ 'a' para agregar nuevas URLs sin borrar las anteriores
            for url in urls_nuevas:
                f.write(url + "\n")
        print(f"✅ {len(urls_nuevas)} URLs añadidas a '{ruta}' para futuras referencias.")

# 🔹 1️⃣ Obtener todos los archivos de sitemap desde el sitemap index
sitemaps_encontrados = obtener_sitemaps(sitemap_index_url)
print(f"🔍 Se encontraron {len(sitemaps_encontrados)} sitemaps.")

# 🔹 2️⃣ Extraer todas las URLs de los sitemaps
urls_extraidas = obtener_urls_de_sitemaps(sitemaps_encontrados)
print(f"✅ Total de URLs extraídas: {len(urls_extraidas)}")

# 🔹 3️⃣ Leer el archivo de URLs indexadas y filtrar las nuevas
urls_indexadas = leer_urls_indexadas(ruta_indexadas)
urls_nuevas = urls_extraidas - urls_indexadas

# 🔹 4️⃣ Guardar solo las nuevas URLs en `urls_por_indexar.txt` para ser enviadas
guardar_urls_nuevas(ruta_por_indexar, urls_nuevas)

# 🔹 5️⃣ Actualizar `urls_indexadas.txt` con las nuevas URLs enviadas
actualizar_urls_indexadas(ruta_indexadas, urls_nuevas)
