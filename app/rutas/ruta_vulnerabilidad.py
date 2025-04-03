from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.base_datos import obtener_bd
from app.esquemas.vulnerabilidad_esquemas import (
    VulnerabilidadCrear,
    VulnerabilidadActualizar
)
from app.servicios.vulnerabilidad_servicio import (
    crear_vulnerabilidad,
    listar_vulnerabilidades,
    actualizar_vulnerabilidad,
    eliminar_vulnerabilidad
)

router = APIRouter(
    prefix="/vulnerabilidades",
    tags=["Vulnerabilidades"]
)

@router.post("/crear")
def crear_vulnerabilidad_endpoint(datos: VulnerabilidadCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_vulnerabilidad(datos, db)
    return {"message": "Vulnerabilidad registrada correctamente", "data": resultado}

@router.get("/listar")
def listar_vulnerabilidades_endpoint(db: Session = Depends(obtener_bd)):
    datos = listar_vulnerabilidades(db)
    return {"message": "Lista de vulnerabilidades", "data": datos}

@router.put("/actualizar/{vuln_id}")
def actualizar_vulnerabilidad_endpoint(vuln_id: int, datos: VulnerabilidadActualizar, db: Session = Depends(obtener_bd)):
    actualizada = actualizar_vulnerabilidad(vuln_id, datos, db)
    return {"message": "Vulnerabilidad actualizada", "data": actualizada}

@router.delete("/eliminar/{vuln_id}")
def eliminar_vulnerabilidad_endpoint(vuln_id: int, db: Session = Depends(obtener_bd)):
    eliminar_vulnerabilidad(vuln_id, db)
    return {"message": "Vulnerabilidad eliminada"}
