from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime
import threading
import time
from app.servicios.configuracion_servicio import obtener_configuracion_escaneo
from app.utils.nmap_utils import ejecutar_nmap
from app.transacciones.escaneos import procesar_resultados
from app.core.base_datos import obtener_bd_sesion

scheduler = BackgroundScheduler()

def ejecutar_escaneo_programado():
    """
    Ejecuta el escaneo Nmap, guarda los resultados en JSON y los inserta en la BD.
    """
    print(f"[INFO] Ejecutando escaneo programado a las {datetime.now()}")

    # Ejecutar escaneo con Nmap y guardar en JSON
    archivo_resultado = ejecutar_nmap()
    
    if archivo_resultado:
        print(f"[INFO] Escaneo completado. Resultados guardados en {archivo_resultado}")

        # 🚀 **Llamamos a escaneos.py para guardar en la BD**
        db_sesion = obtener_bd_sesion()
        try:
            procesar_resultados(db_sesion, archivo_resultado)
        finally:
            db_sesion.close()
    else:
        print("[ERROR] No se pudo ejecutar el escaneo")

def programar_escaneo():
    """
    Obtiene la configuración de escaneo desde la base de datos y programa la ejecución.
    """
    db_sesion = obtener_bd_sesion()
    try:
        configuracion = obtener_configuracion_escaneo(db_sesion)
    except Exception as e:
        print(f"[ERROR] No se pudo obtener la configuración de escaneo: {e}")
        return
    
    scheduler.remove_all_jobs()  # Elimina tareas previas antes de reprogramar

    if configuracion["tipo_escaneo_id"] == 1:  # Tipo "frecuencia"
        frecuencia_minutos = configuracion["frecuencia_minutos"]
        if frecuencia_minutos:
            scheduler.add_job(
                ejecutar_escaneo_programado,
                'interval',
                minutes=frecuencia_minutos,
                id='escaneo_programado'
            )
            print(f"[INFO] Escaneo programado cada {frecuencia_minutos} minutos.")

    elif configuracion["tipo_escaneo_id"] == 2:  # Tipo "hora_especifica"
        hora_especifica = configuracion["hora_especifica"]
        if hora_especifica:
            hora, minuto, segundo = map(int, hora_especifica.split(":"))
            scheduler.add_job(
                ejecutar_escaneo_programado,
                'cron',
                hour=hora,
                minute=minuto,
                second=segundo,
                id='escaneo_programado'
            )
            print(f"[INFO] Escaneo programado a las {hora_especifica} todos los días.")

    else:
        print("[ERROR] Tipo de escaneo no reconocido. No se programará ninguna tarea.")

    db_sesion.close()

def iniciar_programador():
    """
    Inicia el programador en un hilo separado y configura los escaneos.
    """
    scheduler.start()
    print("[INFO] Programador de tareas iniciado.")

    # Monitorear cambios en la configuración cada 30 segundos
    def monitor_configuracion():
        while True:
            time.sleep(30)
            print("[INFO] Revisando configuración de escaneo...")
            programar_escaneo()

    threading.Thread(target=monitor_configuracion, daemon=True).start()
