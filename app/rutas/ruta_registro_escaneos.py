from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.servicios.registro_escaneos_servicio import (
    crear_registro_escaneo, 
    obtener_registro_escaneo, 
    listar_registros_escaneos,
    actualizar_estado_registro_escaneo
)
from app.esquemas.registro_escaneos_esquemas import RegistroEscaneoActualizarEstado

router = APIRouter(
    prefix="/registro_escaneos",
    tags=["Registro de Escaneos"]
)

## ✅ 1️⃣ CREAR UN NUEVO REGISTRO DE ESCANEO
@router.post("/crear_registro_escaneo/{configuracion_escaneo_id}")
def crear_registro_escaneo_endpoint(configuracion_escaneo_id: int, db: Session = Depends(obtener_bd)):
    """
    📌 Crea un nuevo registro de escaneo basado en una configuración de escaneo existente.
    """
    resultado = crear_registro_escaneo(configuracion_escaneo_id, db)
    return {"mensaje": "Registro de escaneo creado exitosamente", "data": resultado}

## ✅ 2️⃣ OBTENER UN REGISTRO DE ESCANEO POR SU ID
@router.get("/obtener_registro_escaneo/{registro_escaneo_id}")
def obtener_registro_escaneo_endpoint(registro_escaneo_id: int, db: Session = Depends(obtener_bd)):
    """
    📌 Obtiene un registro de escaneo específico por su ID.
    """
    resultado = obtener_registro_escaneo(registro_escaneo_id, db)
    return {"mensaje": "Registro de escaneo obtenido exitosamente", "data": resultado}

## ✅ 3️⃣ LISTAR TODOS LOS REGISTROS DE ESCANEOS
@router.get("/listar_registros_escaneos")
def listar_registros_escaneos_endpoint(db: Session = Depends(obtener_bd)):
    """
    📌 Obtiene la lista de todos los registros de escaneos realizados.
    """
    resultado = listar_registros_escaneos(db)
    return {"mensaje": "Lista de registros de escaneos obtenida exitosamente", "data": resultado}

## ✅ 4️⃣ ACTIVAR / DESACTIVAR UN REGISTRO DE ESCANEO
@router.put("/actualizar_estado_registro_escaneo/{registro_escaneo_id}")
def actualizar_estado_registro_escaneo_endpoint(registro_escaneo_id: int, datos: RegistroEscaneoActualizarEstado, db: Session = Depends(obtener_bd)):
    """
    📌 Permite activar o desactivar un registro de escaneo.
    """
    resultado = actualizar_estado_registro_escaneo(registro_escaneo_id, datos, db)
    return {"mensaje": "Estado del registro de escaneo actualizado exitosamente", "data": resultado}
