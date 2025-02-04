# app/core/base_datos.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.config.bd_configuracion import URL_BASE_DATOS
from app.core.respuestas import excepcion_conexion_bd, excepcion_error_bd

try:
    # Crear el motor de la base de datos
    motor = create_engine(URL_BASE_DATOS)
    print("Conexión exitosa con la base de datos.")
except OperationalError as e:
    print(f"Error al conectar con la base de datos: {e}")
    excepcion_conexion_bd()

# Crear la sesión
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)

# Función para obtener una sesión
def obtener_bd():
    bd = SesionLocal()
    try:
        yield bd
    except Exception as e:
        print(f"Error durante la sesión de base de datos: {e}")
        excepcion_error_bd(str(e))
    finally:
        bd.close()
