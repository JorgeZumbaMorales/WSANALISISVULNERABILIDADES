from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.vulnerabilidad import Vulnerabilidad
from app.esquemas.vulnerabilidad_esquemas import (
    VulnerabilidadCrear,
    VulnerabilidadActualizar
)

def crear_vulnerabilidad(datos: VulnerabilidadCrear, db: Session):
    existente = db.query(Vulnerabilidad).filter(Vulnerabilidad.cve_id == datos.cve_id).first()
    if existente:
        # Si existe, actualiza si cambia algo
        actualizado = False
        if datos.score is not None and existente.score != datos.score:
            existente.score = datos.score
            actualizado = True
        if datos.url and existente.url != datos.url:
            existente.url = datos.url
            actualizado = True
        if datos.estado is not None and existente.estado != datos.estado:
            existente.estado = datos.estado
            actualizado = True

        if actualizado:
            db.commit()
            db.refresh(existente)
        return existente

    nueva = Vulnerabilidad(
        cve_id=datos.cve_id,
        score=datos.score,
        url=datos.url,
        estado=datos.estado
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_vulnerabilidades(db: Session):
    return db.query(Vulnerabilidad).all()

def actualizar_vulnerabilidad(vuln_id: int, datos: VulnerabilidadActualizar, db: Session):
    vulnerabilidad = db.query(Vulnerabilidad).filter(Vulnerabilidad.vulnerabilidad_id == vuln_id).first()
    if not vulnerabilidad:
        raise HTTPException(status_code=404, detail="Vulnerabilidad no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(vulnerabilidad, key, value)

    db.commit()
    db.refresh(vulnerabilidad)
    return vulnerabilidad

def eliminar_vulnerabilidad(vuln_id: int, db: Session):
    vulnerabilidad = db.query(Vulnerabilidad).filter(Vulnerabilidad.vulnerabilidad_id == vuln_id).first()
    if not vulnerabilidad:
        raise HTTPException(status_code=404, detail="Vulnerabilidad no encontrada")

    db.delete(vulnerabilidad)
    db.commit()
    return {"message": "Vulnerabilidad eliminada correctamente"}
