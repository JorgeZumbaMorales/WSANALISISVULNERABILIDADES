from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.servicios.configuracion_horas_escaneo_servicio import (
    crear_hora_escaneo, obtener_hora_escaneo,
    actualizar_hora_escaneo, listar_horas_escaneo, eliminar_hora_escaneo
)
from app.esquemas.configuracion_horas_escaneo_esquemas import (
    ConfiguracionHorasEscaneoCrear, ConfiguracionHorasEscaneoActualizar
)

router = APIRouter(
    prefix="/configuracion_horas_escaneo",
    tags=["Horas de Configuración de Escaneos"]
)

## ✅ 1️⃣ CREAR UNA NUEVA HORA DE ESCANEO
@router.post("/crear_hora_escaneo")
def crear_hora_escaneo_endpoint(datos: ConfiguracionHorasEscaneoCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_hora_escaneo(datos, db)
    return {"mensaje": "Hora de escaneo creada exitosamente", "data": resultado}

## ✅ 2️⃣ OBTENER UNA HORA DE ESCANEO POR ID
@router.get("/obtener_hora_escaneo/{id}")
def obtener_hora_escaneo_endpoint(id: int, db: Session = Depends(obtener_bd)):
    resultado = obtener_hora_escaneo(id, db)
    return {"mensaje": "Hora de escaneo obtenida exitosamente", "data": resultado}

## ✅ 3️⃣ ACTUALIZAR UNA HORA DE ESCANEO
@router.put("/actualizar_hora_escaneo/{id}")
def actualizar_hora_escaneo_endpoint(id: int, datos: ConfiguracionHorasEscaneoActualizar, db: Session = Depends(obtener_bd)):
    resultado = actualizar_hora_escaneo(id, datos, db)
    return {"mensaje": "Hora de escaneo actualizada exitosamente", "data": resultado}

## ✅ 4️⃣ LISTAR TODAS LAS HORAS DE UNA CONFIGURACIÓN
@router.get("/listar_horas_escaneo/{configuracion_escaneo_id}")
def listar_horas_escaneo_endpoint(configuracion_escaneo_id: int, db: Session = Depends(obtener_bd)):
    resultado = listar_horas_escaneo(configuracion_escaneo_id, db)
    return {"mensaje": "Lista de horas obtenida exitosamente", "data": resultado}

## ✅ 5️⃣ ELIMINAR UNA HORA DE ESCANEO
@router.delete("/eliminar_hora_escaneo/{id}")
def eliminar_hora_escaneo_endpoint(id: int, db: Session = Depends(obtener_bd)):
    resultado = eliminar_hora_escaneo(id, db)
    return {"mensaje": "Hora de escaneo eliminada exitosamente"}
