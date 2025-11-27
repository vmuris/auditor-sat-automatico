import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# URL Principal del SAT con los listados
URL_SAT = "http://omawww.sat.gob.mx/cifras_sat/Paginas/DatosAbiertos/contribuyentes_publicados.html"
# URL Directa del 69-B (Este es el más importante y a veces no sale en el scraping directo)
URL_69B = "http://omawww.sat.gob.mx/cifras_sat/Documents/Listado_Completo_69-B.csv"

def descargar_archivo(url, nombre_local):
    print(f"⬇️ Intentando descargar: {nombre_local}...")
    try:
        # User-Agent para que el SAT no nos bloquee
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        r = requests.get(url, headers=headers, timeout=60)
        
        if r.status_code == 200:
            with open(nombre_local, 'wb') as f:
                f.write(r.content)
            print(f"✅ Guardado: {nombre_local}")
            return True
        else:
            print(f"❌ Error {r.status_code} al descargar {url}")
            return False
    except Exception as e:
        print(f"❌ Fallo crítico: {e}")
        return False

def main():
    # 1. Descargar el "Padre de todos los listados": El 69-B (EFOS)
    descargar_archivo(URL_69B, "Listado_69B_Definitivo.csv")

    # 2. Buscar otros listados en la página HTML (Art. 69, Condonados, etc.)
    print(f"🔎 Analizando página del SAT: {URL_SAT}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(URL_SAT, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Buscar todos los links que terminen en .csv
        links = soup.find_all('a', href=True)
        count = 0
        
        for link in links:
            href = link['href']
            text = link.text.strip().replace(" ", "_").replace("/", "-")
            
            if href.lower().endswith('.csv'):
                # Corregir URLs relativas si es necesario
                if not href.startswith('http'):
                    full_url = "http://omawww.sat.gob.mx" + href
                else:
                    full_url = href
                
                # Nombre del archivo basado en el texto del link
                nombre_archivo = f"SAT_{text}.csv"
                # Limpieza de nombre
                nombre_archivo = "".join([c for c in nombre_archivo if c.isalnum() or c in "._-"])
                
                descargar_archivo(full_url, nombre_archivo)
                count += 1
                
        print(f"🏁 Proceso terminado. Se intentaron descargar {count} listados adicionales.")

    except Exception as e:
        print(f"Error analizando la página web: {e}")

if __name__ == "__main__":
    main()
