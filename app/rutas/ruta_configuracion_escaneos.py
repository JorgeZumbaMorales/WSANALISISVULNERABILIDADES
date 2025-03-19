from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.servicios.configuracion_escaneos_servicio import (
    crear_configuracion_escaneo, obtener_configuracion_escaneo,
    actualizar_configuracion_escaneo, listar_configuraciones_escaneo, eliminar_configuracion_escaneo
)
from app.esquemas.configuracion_escaneos_esquemas import (
    ConfiguracionEscaneoCrear, ConfiguracionEscaneoActualizar
)

router = APIRouter(
    prefix="/configuracion_escaneos",
    tags=["Configuración de Escaneos"]
)

## ✅ 1️⃣ CREAR UNA NUEVA CONFIGURACIÓN DE ESCANEO
@router.post("/crear_configuracion_escaneo")
def crear_configuracion_escaneo_endpoint(datos: ConfiguracionEscaneoCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_configuracion_escaneo(datos, db)
    return {"mensaje": "Configuración de escaneo creada exitosamente", "data": resultado}

## ✅ 2️⃣ OBTENER UNA CONFIGURACIÓN DE ESCANEO POR ID
@router.get("/obtener_configuracion_escaneo/{configuracion_id}")
def obtener_configuracion_escaneo_endpoint(configuracion_id: int, db: Session = Depends(obtener_bd)):
    resultado = obtener_configuracion_escaneo(configuracion_id, db)
    return {"mensaje": "Configuración de escaneo obtenida exitosamente", "data": resultado}

## ✅ 3️⃣ ACTUALIZAR UNA CONFIGURACIÓN DE ESCANEO
@router.put("/actualizar_configuracion_escaneo/{configuracion_id}")
def actualizar_configuracion_escaneo_endpoint(configuracion_id: int, datos: ConfiguracionEscaneoActualizar, db: Session = Depends(obtener_bd)):
    resultado = actualizar_configuracion_escaneo(configuracion_id, datos, db)
    return {"mensaje": "Configuración de escaneo actualizada exitosamente", "data": resultado}

## ✅ 4️⃣ LISTAR TODAS LAS CONFIGURACIONES
@router.get("/listar_configuraciones_escaneo")
def listar_configuraciones_escaneo_endpoint(db: Session = Depends(obtener_bd)):
    resultado = listar_configuraciones_escaneo(db)
    return {"mensaje": "Lista de configuraciones de escaneo obtenida exitosamente", "data": resultado}

## ✅ 5️⃣ ELIMINAR UNA CONFIGURACIÓN DE ESCANEO
@router.delete("/eliminar_configuracion_escaneo/{configuracion_id}")
def eliminar_configuracion_escaneo_endpoint(configuracion_id: int, db: Session = Depends(obtener_bd)):
    resultado = eliminar_configuracion_escaneo(configuracion_id, db)
    return {"mensaje": "Configuración de escaneo eliminada exitosamente"}
