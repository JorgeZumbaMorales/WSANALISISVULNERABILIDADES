from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.servicios.configuracion_escaneo_servicio import (
    crear_configuracion_escaneo, 
    actualizar_configuracion_escaneo, 
    eliminar_configuracion_escaneo,
    obtener_configuracion_actual,
    listar_configuraciones
)
from app.esquemas.configuracion_escaneo_esquemas import ConfiguracionEscaneoCrear, ConfiguracionEscaneoActualizar

router = APIRouter(
    prefix="/configuracion_escaneo",
    tags=["Configuración de Escaneo"]
)

@router.post("/")
def crear_configuracion_escaneo_endpoint(datos: ConfiguracionEscaneoCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_configuracion_escaneo(datos, db)
    return {"message": "Configuración de escaneo creada exitosamente", "data": resultado}

@router.put("/{configuracion_id}")
def actualizar_configuracion_escaneo_endpoint(configuracion_id: int, datos: ConfiguracionEscaneoActualizar, db: Session = Depends(obtener_bd)):
    resultado = actualizar_configuracion_escaneo(configuracion_id, datos, db)
    return {"message": "Configuración de escaneo actualizada", "data": resultado}

@router.delete("/{configuracion_id}")
def eliminar_configuracion_escaneo_endpoint(configuracion_id: int, db: Session = Depends(obtener_bd)):
    eliminar_configuracion_escaneo(configuracion_id, db)
    return {"message": "Configuración de escaneo eliminada exitosamente"}

@router.get("/actual")
def obtener_configuracion_actual_endpoint(db: Session = Depends(obtener_bd)):
    configuracion = obtener_configuracion_actual(db)
    return {"message": "Configuración activa obtenida", "data": configuracion}

@router.get("/")
def listar_configuraciones_endpoint(db: Session = Depends(obtener_bd)):
    configuraciones = listar_configuraciones(db)
    return {"message": "Lista de configuraciones obtenida", "data": configuraciones}
