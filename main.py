import requests
import pdfplumber
import re
import pandas as pd
import os

# Configuración
url = "https://www.sat.gob.mx/minisitio/PadronImportadoresExportadores/documentos/Pad_Exp_Sec.pdf"
pdf_temp = "Padron_SAT.pdf"
csv_salida = "BD_PADRON_SAT.csv"

print("⬇️ Descargando PDF del SAT...")
# Usamos Headers para parecer un navegador real y evitar bloqueos
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(url, headers=headers)
with open(pdf_temp, 'wb') as f:
    f.write(response.content)

print("📖 Procesando PDF...")
rfc_pattern = re.compile(r'[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}')
all_rfcs = []

try:
    with pdfplumber.open(pdf_temp) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                clean_text = text.replace('\n', '').replace(' ', '')
                found = rfc_pattern.findall(clean_text) 
                all_rfcs.extend(found)

    # Limpiar duplicados y Guardar
    unique_rfcs = list(set(all_rfcs))
    unique_rfcs.sort()
    
    df = pd.DataFrame(unique_rfcs, columns=["RFC"])
    df.to_csv(csv_salida, index=False)
    print(f"✅ ÉXITO: {len(unique_rfcs)} RFCs guardados.")

except Exception as e:
    print(f"❌ Error: {e}")
    exit(1) # Forzar error para que GitHub avise
