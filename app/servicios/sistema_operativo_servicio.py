from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.sistema_operativo import SistemaOperativo
from app.esquemas.sistema_operativo_esquemas import SistemaOperativoCrear, SistemaOperativoActualizar

def crear_sistema_operativo(datos_so: SistemaOperativoCrear, db: Session):
    nuevo_so = SistemaOperativo(
        nombre_so=datos_so.nombre_so,
        estado=datos_so.estado
    )
    db.add(nuevo_so)
    db.commit()
    db.refresh(nuevo_so)
    return nuevo_so

def listar_sistemas_operativos(db: Session):
    return db.query(SistemaOperativo).all()

def actualizar_sistema_operativo(so_id: int, datos_so: SistemaOperativoActualizar, db: Session):
    so_existente = db.query(SistemaOperativo).filter(SistemaOperativo.sistema_operativo_id == so_id).first()
    if not so_existente:
        raise HTTPException(status_code=404, detail="Sistema operativo no encontrado")
    
    for key, value in datos_so.dict(exclude_unset=True).items():
        setattr(so_existente, key, value)
    
    db.commit()
    db.refresh(so_existente)
    return so_existente

def eliminar_sistema_operativo(so_id: int, db: Session):
    so_existente = db.query(SistemaOperativo).filter(SistemaOperativo.sistema_operativo_id == so_id).first()
    if not so_existente:
        raise HTTPException(status_code=404, detail="Sistema operativo no encontrado")
    
    db.delete(so_existente)
    db.commit()
    return {"message": "Sistema operativo eliminado exitosamente"}
