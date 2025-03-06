from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.esquemas.sistema_operativo_esquemas import (
    SistemaOperativoCrear, 
    SistemaOperativoActualizar
)
from app.servicios.sistema_operativo_servicio import (
    crear_sistema_operativo,
    listar_sistemas_operativos,
    actualizar_sistema_operativo,
    eliminar_sistema_operativo
)

router = APIRouter(
    prefix="/sistemas_operativos",
    tags=["Sistemas Operativos"]
)

@router.post("/crear_sistema_operativo")
def crear_sistema_operativo_endpoint(datos_so: SistemaOperativoCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_sistema_operativo(datos_so, db)
    return {"message": "Sistema operativo creado correctamente", "data": resultado}

@router.get("/listar_sistemas_operativos")
def listar_sistemas_operativos_endpoint(db: Session = Depends(obtener_bd)):
    sistemas = listar_sistemas_operativos(db)
    return {"message": "Lista de sistemas operativos obtenida exitosamente", "data": sistemas}

@router.put("/actualizar_sistema_operativo/{so_id}")
def actualizar_sistema_operativo_endpoint(so_id: int, datos_so: SistemaOperativoActualizar, db: Session = Depends(obtener_bd)):
    sistema = actualizar_sistema_operativo(so_id, datos_so, db)
    if not sistema:
        raise HTTPException(status_code=404, detail="Sistema operativo no encontrado")
    return {"message": "Sistema operativo actualizado exitosamente", "data": sistema}

@router.delete("/eliminar_sistema_operativo/{so_id}")
def eliminar_sistema_operativo_endpoint(so_id: int, db: Session = Depends(obtener_bd)):
    eliminar_sistema_operativo(so_id, db)
    return {"message": "Sistema operativo eliminado exitosamente"}
