import psycopg2
import re

# 📂 Ruta del archivo nmap-os-db (ajusta si es necesario)
NMAP_DB_PATH = "nmap-os-db"

# 📌 Conexión a la base de datos PostgreSQL
DB_CONFIG = {
    "dbname": "web_app_db",
    "user": "jorgezumbamorales",
    "password": "Espoch1.",
    "host": "localhost",
    "port": "5432"
}

def extraer_sistemas_operativos():
    """Extrae los nombres de los sistemas operativos del archivo nmap-os-db"""
    sistemas_operativos = set()  # Usamos un set para evitar duplicados

    with open(NMAP_DB_PATH, "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(r"Fingerprint\s+(.+)", line)  # Busca líneas que comienzan con "Fingerprint"
            if match:
                sistema_operativo = match.group(1).strip()
                sistemas_operativos.add(sistema_operativo)

    return list(sistemas_operativos)

def insertar_sistemas_operativos():
    """Inserta los sistemas operativos en la base de datos"""
    sistemas_operativos = extraer_sistemas_operativos()
    
    if not sistemas_operativos:
        print("⚠️ No se encontraron sistemas operativos en el archivo.")
        return

    print(f"🔹 Se encontraron {len(sistemas_operativos)} sistemas operativos únicos.")

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for so in sistemas_operativos:
            cursor.execute(
                """
                INSERT INTO gestion_dispositivos.sistemas_operativos (nombre_so, fecha_creacion, estado) 
                VALUES (%s, NOW(), TRUE) 
                ON CONFLICT (nombre_so) DO NOTHING;
                """,
                (so,)
            )

        conn.commit()
        print("✅ Sistemas operativos insertados correctamente.")
    except Exception as e:
        print(f"⚠️ Error al insertar en la base de datos: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("📥 Extrayendo sistemas operativos de nmap-os-db...")
    insertar_sistemas_operativos()
