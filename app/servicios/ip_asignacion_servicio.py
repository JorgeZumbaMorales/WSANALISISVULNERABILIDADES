from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.ip_asignacion import IpAsignacion
from app.esquemas.ip_asignacion_esquemas import IpAsignacionCrear, IpAsignacionActualizar

def crear_ip_asignacion(datos: IpAsignacionCrear, db: Session):
    nueva_ip = IpAsignacion(
        dispositivo_id=datos.dispositivo_id,
        ip_address=datos.ip_address,
        estado=datos.estado
    )
    db.add(nueva_ip)
    db.commit()
    db.refresh(nueva_ip)
    return nueva_ip

def listar_ip_asignaciones(db: Session):
    return db.query(IpAsignacion).all()

def actualizar_ip_asignacion(ip_id: int, datos: IpAsignacionActualizar, db: Session):
    ip_existente = db.query(IpAsignacion).filter(IpAsignacion.ip_asignacion_id == ip_id).first()
    if not ip_existente:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(ip_existente, key, value)
    
    db.commit()
    db.refresh(ip_existente)
    return ip_existente

def eliminar_ip_asignacion(ip_id: int, db: Session):
    ip_existente = db.query(IpAsignacion).filter(IpAsignacion.ip_asignacion_id == ip_id).first()
    if not ip_existente:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    db.delete(ip_existente)
    db.commit()
    return {"message": "Registro eliminado exitosamente"}
