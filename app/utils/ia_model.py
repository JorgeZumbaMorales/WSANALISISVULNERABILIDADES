import json
import pandas as pd
import numpy as np
import requests
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# 📂 **Cargar datos desde el archivo JSON generado por Nmap**
def cargar_datos(nombre_archivo="nmap_resultados.json"):
    with open(nombre_archivo, "r") as file:
        datos = json.load(file)
    return datos

# 🔹 **Consultar Fabricante de la MAC usando API**
def obtener_fabricante(mac):
    try:
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url)
        return response.text if response.status_code == 200 else "Desconocido"
    except Exception as e:
        print(f"Error en MAC Vendors API: {e}")
        return "Desconocido"

# 🔹 **Consultar Nmap OS Database**
def obtener_info_sistema_operativo(fingerprint):
    try:
        # Se usa la base de datos local de Nmap (preinstalada con Nmap)
        NMAP_DB_PATH = "/usr/share/nmap/nmap-os-db"
        with open(NMAP_DB_PATH, "r", encoding="utf-8") as db:
            db_content = db.read()
        coincidencias = [line for line in db_content.split("\n") if fingerprint[:10] in line]
        return coincidencias[0] if coincidencias else "Desconocido"
    except Exception as e:
        print(f"Error accediendo a la base de datos de Nmap: {e}")
        return "Desconocido"

# 🔹 **Consultar Shodan API para detalles de seguridad** (Requiere API KEY)
def consultar_shodan(ip):
    SHODAN_API_KEY = "6DLQExWWXQVjHcehgQbDbumvoaLiCgjR"  # Reemplaza con tu API Key de Shodan
    try:
        url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "vulnerabilidades": data.get("vulns", []),
                "puertos_detectados": data.get("ports", []),
                "organizacion": data.get("org", "Desconocido"),
                "sistema_operativo": data.get("os", "Desconocido")
            }
        return {"vulnerabilidades": [], "puertos_detectados": [], "organizacion": "Desconocido", "sistema_operativo": "Desconocido"}
    except Exception as e:
        print(f"Error en Shodan API: {e}")
        return {"vulnerabilidades": [], "puertos_detectados": [], "organizacion": "Desconocido", "sistema_operativo": "Desconocido"}

# 🔹 **Consultar CVE Database (NVD) para vulnerabilidades conocidas**
def consultar_cve(servicio, version):
    NVD_API_KEY = "706bf6d8-c578-4bc4-8a36-68a625858828"  # Reemplaza con tu API Key de NVD
    try:
        url = f"https://services.nvd.nist.gov/rest/json/cves/1.0"
        params = {
            "keyword": f"{servicio} {version}",
            "resultsPerPage": 5,
            "apiKey": NVD_API_KEY
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return len(data.get("result", {}).get("CVE_Items", []))  # Número de CVEs encontrados
        return 0
    except Exception as e:
        print(f"Error en CVE NVD: {e}")
        return 0

# 📊 **Convertir datos en DataFrame**
def procesar_datos(datos):
    df = pd.DataFrame(datos)

    # 🔹 **Enriquecer los datos con bases de datos externas**
    df["fabricante"] = df["mac"].apply(obtener_fabricante)
    df["sistemas_operativos"] = df["fingerprint"].apply(obtener_info_sistema_operativo)
    
    # 🔹 **Consultar Shodan**
    shodan_info = df["ip"].apply(consultar_shodan)
    df["vulnerabilidades_shodan"] = shodan_info.apply(lambda x: len(x["vulnerabilidades"]))
    df["organizacion"] = shodan_info.apply(lambda x: x["organizacion"])
    df["sistema_operativo_shodan"] = shodan_info.apply(lambda x: x["sistema_operativo"])

    # 🔹 **Extraer información de puertos abiertos**
    servicios_unicos = set()
    for dispositivo in datos:
        for puerto in dispositivo["puertos_abiertos"]:
            servicios_unicos.add(puerto["servicio"])

    # 🔹 **Crear columnas para cada servicio detectado**
    for servicio in servicios_unicos:
        df[servicio] = df["puertos_abiertos"].apply(
            lambda puertos: any(p["servicio"] == servicio for p in puertos)
        ).astype(int)

    # 🔹 **Añadir columna de vulnerabilidades CVE por cada servicio**
    for servicio in servicios_unicos:
        df[f"cve_{servicio}"] = df["puertos_abiertos"].apply(
            lambda puertos: sum(consultar_cve(p["servicio"], p["version"]) for p in puertos if p["servicio"] == servicio)
        )

    # 🔹 **Convertir fabricante en un número (Label Encoding)**
    le_fabricante = LabelEncoder()
    df["fabricante"] = le_fabricante.fit_transform(df["fabricante"])

    # 🔹 **Convertir valores 'Desconocido' en NaN**
    df.replace("Desconocido", np.nan, inplace=True)

    # 🔹 **Llenar NaN con valores numéricos para evitar errores en el modelo**
    df.fillna(0, inplace=True)

    # 🔹 **Definir la variable objetivo (y)**
    if "tipo_dispositivo" in df.columns:
        y = df["tipo_dispositivo"]
    else:
        y = ["Desconocido"] * len(df)

    # 🔹 **Eliminar columnas irrelevantes**
    df = df.drop(columns=["ip", "mac", "fingerprint", "puertos_abiertos"])

    return df, y, le_fabricante.classes_


# 🏋️‍♂️ **Entrenar modelo de Machine Learning**
def entrenar_modelo(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    print(f"🎯 Precisión del modelo: {accuracy_score(y_test, y_pred) * 100:.2f}%")

    return modelo

# 🔍 **Predecir el tipo de dispositivo con IA**
def predecir_dispositivo(modelo, datos_nuevos):
    df_nuevo = pd.DataFrame([datos_nuevos])

    for col in X.columns:
        if col not in df_nuevo.columns:
            df_nuevo[col] = 0  

    return modelo.predict(df_nuevo)[0]

# 🚀 **Ejecutar todo el pipeline**
if __name__ == "__main__":
    print("📥 Cargando datos de dispositivos...")
    datos = cargar_datos()

    print("📊 Procesando datos para entrenamiento...")
    X, y, clases_fabricantes = procesar_datos(datos)

    print("🏋️ Entrenando modelo de IA...")
    modelo_entrenado = entrenar_modelo(X, y)

    print("🤖 ¡Modelo entrenado y listo para predecir!")
