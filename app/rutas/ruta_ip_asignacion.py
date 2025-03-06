from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.esquemas.ip_asignacion_esquemas import (
    IpAsignacionCrear, 
    IpAsignacionActualizar
)
from app.servicios.ip_asignacion_servicio import (
    crear_ip_asignacion,
    listar_ip_asignaciones,
    actualizar_ip_asignacion,
    eliminar_ip_asignacion
)

router = APIRouter(
    prefix="/ip_asignaciones",
    tags=["IP Asignaciones"]
)

@router.post("/crear")
def crear_ip_asignacion_endpoint(datos: IpAsignacionCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_ip_asignacion(datos, db)
    return {"message": "IP asignada correctamente", "data": resultado}

@router.get("/listar")
def listar_ip_asignaciones_endpoint(db: Session = Depends(obtener_bd)):
    registros = listar_ip_asignaciones(db)
    return {"message": "Lista de asignaciones obtenida exitosamente", "data": registros}

@router.put("/actualizar/{ip_id}")
def actualizar_ip_asignacion_endpoint(ip_id: int, datos: IpAsignacionActualizar, db: Session = Depends(obtener_bd)):
    registro = actualizar_ip_asignacion(ip_id, datos, db)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"message": "Registro actualizado exitosamente", "data": registro}

@router.delete("/eliminar/{ip_id}")
def eliminar_ip_asignacion_endpoint(ip_id: int, db: Session = Depends(obtener_bd)):
    eliminar_ip_asignacion(ip_id, db)
    return {"message": "Registro eliminado exitosamente"}
