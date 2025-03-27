from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime
import threading
import time
from app.core.base_datos import SesionLocal
from app.servicios.configuracion_escaneos_servicio import obtener_configuracion_escaneo_con_horas
from app.utils.nmap_utils import ejecutar_nmap
from app.transacciones.transaccion_guardar_escaneos import procesar_resultados
from app.servicios.registro_escaneos_servicio import crear_registro_escaneo

scheduler = BackgroundScheduler()

def obtener_configuracion_escaneo_activa(db: Session):
    """
    📌 Obtiene la configuración de escaneo activa con sus horas si es necesario.
    """
    return obtener_configuracion_escaneo_con_horas(db)


def ejecutar_escaneo_programado():
    """
    📌 Ejecuta un escaneo según la configuración activa.
    """
    print("[DEBUG] 📢 Intentando ejecutar el escaneo programado...")
    db_sesion = SesionLocal()
    
    try:
        configuracion_activa = obtener_configuracion_escaneo_activa(db_sesion)
        
        if not configuracion_activa:
            print("[INFO] ❌ No hay configuración activa. No se ejecutará el escaneo.")
            return
        
        print(f"[INFO] 🔄 Ejecutando escaneo con la configuración: {configuracion_activa.nombre_configuracion_escaneo}")

        # ✅ Registrar ejecución en la BD
        registro_escaneo = crear_registro_escaneo(configuracion_activa.configuracion_escaneo_id, db_sesion)
        db_sesion.commit()

        # ✅ Cerrar la sesión antes de ejecutar el escaneo
        db_sesion.close()

        # ✅ Ejecutar escaneo
        archivo_resultado = ejecutar_nmap()
        if not archivo_resultado:
            print("[ERROR] ❌ No se pudo ejecutar el escaneo.")
            return

        print(f"[INFO] ✅ Escaneo completado. Resultados guardados en {archivo_resultado}")

        # ✅ Guardar resultados
        with SesionLocal() as nueva_sesion:
            procesar_resultados(nueva_sesion, archivo_resultado)
            nueva_sesion.commit()

    except Exception as e:
        print(f"[ERROR] ❌ Error en la ejecución del escaneo: {str(e)}")
        db_sesion.rollback()

    finally:
        if db_sesion.is_active:
            db_sesion.close()

    print(f"[DEBUG] 📋 Tareas programadas tras ejecución: {scheduler.get_jobs()}")


def programar_escaneo():
    """
    📌 Configura la programación de escaneos según la configuración activa en la BD.
    """
    db_sesion = SesionLocal()
    try:
        configuracion_activa = obtener_configuracion_escaneo_activa(db_sesion)

        if not configuracion_activa:
            print("[INFO] ❌ No hay configuración activa. No se programará ningún escaneo.")
            return

        # ✅ Cancelar tareas previas antes de programar la nueva
        scheduler.remove_all_jobs()

        print("[INFO] ✅ Programando nuevo escaneo.")

        # ✅ Configurar tipo de escaneo
        if configuracion_activa.tipo_escaneo_id == 1:  # Tipo "Frecuencia"
            frecuencia_minutos = configuracion_activa.frecuencia_minutos
            if isinstance(frecuencia_minutos, int) and frecuencia_minutos > 0:
                scheduler.add_job(
                    ejecutar_escaneo_programado,
                    'interval',
                    minutes=frecuencia_minutos,
                    id='escaneo_programado'
                )
                print(f"[INFO] ✅ Escaneo programado cada {frecuencia_minutos} minutos.")
            else:
                print(f"[ERROR] ❌ Frecuencia de escaneo no válida: {frecuencia_minutos}")

        elif configuracion_activa.tipo_escaneo_id == 2:  # Tipo "Escaneo en Horas Específicas"
            # 🔹 Obtener lista de horas asociadas
            horas_escaneo = configuracion_activa.horas_escaneo
            if not horas_escaneo:
                print("[ERROR] ❌ No hay horas definidas para este escaneo. No se programará nada.")
                return

            for hora_obj in horas_escaneo:
                h, m, s = map(int, str(hora_obj.hora).split(":"))
                scheduler.add_job(
                    ejecutar_escaneo_programado,
                    'cron',
                    hour=h,
                    minute=m,
                    second=s
                )
                print(f"[INFO] ✅ Escaneo programado a las {hora_obj.hora}.")

        print(f"[DEBUG] 📋 Tareas programadas: {scheduler.get_jobs()}")

    finally:
        db_sesion.close()


def iniciar_programador():
    """
    📌 Inicia el programador en un hilo separado y revisa cambios en la configuración.
    """
    scheduler.start()
    print("[INFO] ✅ Programador de tareas iniciado.")

    # 🔄 Forzar ejecución de prueba en 10 segundos
    """
    print("[INFO] 🔄 Forzando ejecución de prueba en 10 segundos...")
    scheduler.add_job(
        ejecutar_escaneo_programado,
        'date',
        run_date=datetime.now(),
        id="test_run"
    )
     """
    
    # 🔄 Monitorear cambios cada 30 segundos
    def monitor_configuracion():
        """
        🔄 Revisar cambios en la configuración y evitar que el programador se detenga.
        """
        while True:
            time.sleep(30)
            print("[INFO] 🔄 Revisando cambios en la configuración de escaneo...")
            programar_escaneo()

            # 🟢 Verificar si el programador sigue activo
            if not scheduler.running:
                print("[WARNING] ❌ El programador estaba detenido. Reiniciando...")
                scheduler.start()

            jobs = scheduler.get_jobs()
            if not jobs:
                print("[WARNING] ❌ No hay tareas programadas. Intentando reprogramar...")
                programar_escaneo()

            print(f"[DEBUG] 🟢 Estado del programador: {scheduler.running}")
            print(f"[DEBUG] 📋 Tareas programadas actualmente: {scheduler.get_jobs()}")

    threading.Thread(target=monitor_configuracion, daemon=True).start()
