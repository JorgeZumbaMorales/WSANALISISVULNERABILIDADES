from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from app.modelos.dispositivo import Dispositivo
from app.esquemas.dispositivo_esquemas import DispositivoCrear, DispositivoActualizar
from app.modelos.dispositivo_sistema_operativo import DispositivoSistemaOperativo
from app.modelos.sistema_operativo import SistemaOperativo
from app.modelos.ip_asignaciones import IpAsignacion

def crear_dispositivo(datos_dispositivo: DispositivoCrear, db: Session):
    dispositivo_existente = db.query(Dispositivo).filter(Dispositivo.mac_address == datos_dispositivo.mac_address).first()
    if dispositivo_existente:
        raise HTTPException(status_code=400, detail="Ya existe un dispositivo con esta MAC")
    
    nuevo_dispositivo = Dispositivo(
        nombre_dispositivo=datos_dispositivo.nombre_dispositivo,
        mac_address=datos_dispositivo.mac_address
    )
    db.add(nuevo_dispositivo)
    db.commit()
    db.refresh(nuevo_dispositivo)
    return nuevo_dispositivo

def listar_dispositivos(db: Session):
    return db.query(Dispositivo).all()

def listar_dispositivos_completo(db: Session):
    """
    Obtiene la lista de dispositivos con su sistema operativo y la última IP asignada.
    """
    dispositivos = db.query(Dispositivo).all()

    dispositivos_resultado = []
    for dispositivo in dispositivos:
        # Obtener el sistema operativo si existe
        so = dispositivo.sistema_operativo_relacion[0].sistema_operativo.nombre_so if dispositivo.sistema_operativo_relacion else "Desconocido"

        # Obtener la última IP asignada
        ultima_ip = (
            db.query(IpAsignacion.ip_address)
            .filter(IpAsignacion.dispositivo_id == dispositivo.dispositivo_id)
            .order_by(IpAsignacion.fecha_creacion.desc())
            .first()
        )
        
        dispositivos_resultado.append({
            "dispositivo_id": dispositivo.dispositivo_id,
            "mac_address": dispositivo.mac_address,
            "sistema_operativo": so,
            "ultima_ip": ultima_ip[0] if ultima_ip else "No asignada",
            "estado": dispositivo.estado
        })

    return dispositivos_resultado


def actualizar_dispositivo(dispositivo_id: int, datos_dispositivo: DispositivoActualizar, db: Session):
    dispositivo_existente = db.query(Dispositivo).filter(Dispositivo.dispositivo_id == dispositivo_id).first()
    if not dispositivo_existente:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    for key, value in datos_dispositivo.dict(exclude_unset=True).items():
        setattr(dispositivo_existente, key, value)
    
    db.commit()
    db.refresh(dispositivo_existente)
    return dispositivo_existente

def eliminar_dispositivo(dispositivo_id: int, db: Session):
    dispositivo_existente = db.query(Dispositivo).filter(Dispositivo.dispositivo_id == dispositivo_id).first()
    if not dispositivo_existente:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    db.delete(dispositivo_existente)
    db.commit()
    return {"message": "Dispositivo eliminado exitosamente"}
