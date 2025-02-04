# app/core/respuestas.py
from fastapi import HTTPException

# Excepción cuando no se puede conectar a la base de datos
def excepcion_conexion_bd():
    raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")

# Excepción cuando ocurre un error general en la base de datos
def excepcion_error_bd(error: str):
    raise HTTPException(status_code=500, detail=f"Error en la base de datos: {error}")

# Excepción cuando un recurso ya existe
def excepcion_recurso_existente(entidad: str):
    raise HTTPException(status_code=400, detail=f"{entidad} ya existe")

# Excepción cuando un recurso no se encuentra
def excepcion_no_encontrado(entidad: str):
    raise HTTPException(status_code=404, detail=f"{entidad} no encontrado")

# Respuesta de éxito para operaciones generales
def respuesta_exitosa(mensaje: str, datos=None):
    respuesta = {"mensaje": mensaje}
    if datos:
        respuesta["datos"] = datos
    return respuesta
