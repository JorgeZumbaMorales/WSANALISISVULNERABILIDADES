from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.esquemas.dispositivo_sistema_operativo_esquemas import (
    DispositivoSistemaOperativoCrear, 
    DispositivoSistemaOperativoActualizar
)
from app.servicios.dispositivo_sistema_operativo_servicio import (
    crear_dispositivo_sistema_operativo,
    listar_dispositivos_sistemas_operativos,
    actualizar_dispositivo_sistema_operativo,
    eliminar_dispositivo_sistema_operativo
)

router = APIRouter(
    prefix="/dispositivo_sistema_operativo",
    tags=["Dispositivo Sistema Operativo"]
)

@router.post("/crear")
def crear_dispositivo_sistema_operativo_endpoint(datos: DispositivoSistemaOperativoCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_dispositivo_sistema_operativo(datos, db)
    return {"message": "Registro creado correctamente", "data": resultado}

@router.get("/listar")
def listar_dispositivos_sistemas_operativos_endpoint(db: Session = Depends(obtener_bd)):
    registros = listar_dispositivos_sistemas_operativos(db)
    return {"message": "Lista de registros obtenida exitosamente", "data": registros}

@router.put("/actualizar/{dispositivo_so_id}")
def actualizar_dispositivo_sistema_operativo_endpoint(dispositivo_so_id: int, datos: DispositivoSistemaOperativoActualizar, db: Session = Depends(obtener_bd)):
    registro = actualizar_dispositivo_sistema_operativo(dispositivo_so_id, datos, db)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"message": "Registro actualizado exitosamente", "data": registro}

@router.delete("/eliminar/{dispositivo_so_id}")
def eliminar_dispositivo_sistema_operativo_endpoint(dispositivo_so_id: int, db: Session = Depends(obtener_bd)):
    eliminar_dispositivo_sistema_operativo(dispositivo_so_id, db)
    return {"message": "Registro eliminado exitosamente"}
