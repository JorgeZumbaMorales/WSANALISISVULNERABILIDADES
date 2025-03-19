from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime
import threading
import time
from app.core.base_datos import SesionLocal
from app.servicios.configuracion_escaneos_servicio import listar_configuraciones_escaneo
from app.utils.nmap_utils import ejecutar_nmap
from app.transacciones.escaneos import procesar_resultados
from app.servicios.registro_escaneos_servicio import crear_registro_escaneo

scheduler = BackgroundScheduler()

def obtener_configuracion_escaneo_activa(db: Session):
    """
    📌 Obtiene la configuración de escaneo activa (la más reciente con estado=True).
    """
    configuraciones = listar_configuraciones_escaneo(db)
    return next((config for config in configuraciones if config.estado), None)


def ejecutar_escaneo_programado():
    """
    📌 Ejecuta un escaneo según la configuración activa.
    """
    db_sesion = SesionLocal()  # ✅ Crear nueva sesión de base de datos
    try:
        print("[DEBUG] 📢 ¡Ejecutando el escaneo programado!")

        configuracion_activa = obtener_configuracion_escaneo_activa(db_sesion)
        
        if not configuracion_activa:
            print("[INFO] No hay una configuración activa. No se ejecutará el escaneo.")
            return

        print(f"[INFO] Ejecutando escaneo con la configuración: {configuracion_activa.nombre_configuracion_escaneo}")

        # ✅ Registrar que se está ejecutando un escaneo
        registro_escaneo = crear_registro_escaneo(configuracion_activa.configuracion_escaneo_id, db_sesion)
        
        db_sesion.commit()  # ✅ Confirmar transacción
        
        # ✅ Cerrar la sesión antes de procesar los resultados para evitar conflictos
        db_sesion.close()

        # ✅ Ejecutar el escaneo con Nmap
        archivo_resultado = ejecutar_nmap()

        if archivo_resultado:
            print(f"[INFO] Escaneo completado. Resultados guardados en {archivo_resultado}")

            # ✅ Crear una nueva sesión para procesar los resultados
            with SesionLocal() as nueva_sesion:
                procesar_resultados(nueva_sesion, archivo_resultado)  # ✅ Nueva sesión para evitar conflictos
                nueva_sesion.commit()

        else:
            print("[ERROR] No se pudo ejecutar el escaneo")

    except Exception as e:
        print(f"[ERROR] ❌ Error en la ejecución del escaneo: {str(e)}")
        db_sesion.rollback()  # ⚠️ Asegurar que no quedan transacciones abiertas

    finally:
        if db_sesion.is_active:
            db_sesion.close()  # ✅ Cerrar la sesión al finalizar


def programar_escaneo():
    """
    📌 Configura la programación de escaneos según la configuración activa en la BD.
    """
    db_sesion = SesionLocal()
    try:
        configuracion_activa = obtener_configuracion_escaneo_activa(db_sesion)

        # 🛑 Si no hay configuración activa, no programamos nada
        if not configuracion_activa:
            print("[INFO] No hay una configuración activa. No se programará ningún escaneo.")
            return

        # 🔄 Eliminamos cualquier tarea programada previamente
        scheduler.remove_all_jobs()

        # ✅ Configurar según el tipo de escaneo
        if configuracion_activa.tipo_escaneo_id == 1:  # Tipo "Frecuencia"
            frecuencia_minutos = configuracion_activa.frecuencia_minutos
            if frecuencia_minutos:
                scheduler.add_job(
                    ejecutar_escaneo_programado,
                    'interval',
                    minutes=frecuencia_minutos,
                    id='escaneo_programado'
                )
                print(f"[INFO] Escaneo programado cada {frecuencia_minutos} minutos.")

        elif configuracion_activa.tipo_escaneo_id == 2:  # Tipo "Hora específica"
            hora_especifica = configuracion_activa.hora_especifica
            if hora_especifica:
                hora, minuto, segundo = map(int, str(hora_especifica).split(":"))
                scheduler.add_job(
                    ejecutar_escaneo_programado,
                    'cron',
                    hour=hora,
                    minute=minuto,
                    second=segundo,
                    id='escaneo_programado'
                )
                print(f"[INFO] Escaneo programado a las {hora_especifica} todos los días.")

        # 🔍 **Verificar si la tarea se agregó correctamente**
        print(f"[DEBUG] Tareas programadas actualmente: {scheduler.get_jobs()}")

    finally:
        db_sesion.close()


def iniciar_programador():
    """
    📌 Inicia el programador en un hilo separado y revisa cambios en la configuración.
    """
    scheduler.start()
    print("[INFO] Programador de tareas iniciado.")

    # 🔄 Forzar la ejecución de una tarea inmediatamente para probar
    print("[INFO] 🔄 Forzando ejecución de prueba en 10 segundos...")
    scheduler.add_job(
        ejecutar_escaneo_programado,
        'date',  # Ejecutar una vez en una fecha específica
        run_date=datetime.now(),
        id="test_run"
    )

    # 🔄 Monitorear cambios en la configuración cada 30 segundos
    def monitor_configuracion():
        while True:
            time.sleep(30)
            print("[INFO] Revisando cambios en la configuración de escaneo...")
            programar_escaneo()

            # 🔍 **Verificar si el programador sigue activo**
            print(f"[DEBUG] Estado del programador: {scheduler.running}")
            print(f"[DEBUG] Tareas programadas: {scheduler.get_jobs()}")

    threading.Thread(target=monitor_configuracion, daemon=True).start()

