from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.base_datos import obtener_bd
from app.esquemas.sistema_operativo_esquemas import (
    SistemaOperativoCrear, 
    SistemaOperativoActualizar,
    SistemaOperativoRespuesta, SistemaOperativoBusqueda
)
from app.servicios.sistema_operativo_servicio import (
    crear_sistema_operativo,
    listar_sistemas_operativos,
    actualizar_sistema_operativo,
    eliminar_sistema_operativo,
    buscar_sistemas_operativos_por_nombre  # ✅ AQUÍ va esta función
)

router = APIRouter(
    prefix="/sistemas_operativos",
    tags=["Sistemas Operativos"]
)

@router.post("/crear_sistema_operativo")
def crear_sistema_operativo_endpoint(datos_so: SistemaOperativoCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_sistema_operativo(datos_so, db)
    return {"message": "Sistema operativo creado correctamente", "data": resultado}

@router.get("/listar_sistemas_operativos", response_model=List[SistemaOperativoRespuesta])
def listar_sistemas_operativos_endpoint(db: Session = Depends(obtener_bd)):
    return listar_sistemas_operativos(db)

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

@router.get("/buscar_sistemas_operativos", response_model=List[SistemaOperativoBusqueda])
def buscar_sistemas_operativos_endpoint(q: str, db: Session = Depends(obtener_bd)):
    resultados = buscar_sistemas_operativos_por_nombre(q, db)
    return resultados
