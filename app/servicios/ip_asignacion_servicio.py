from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.ip_asignaciones import IpAsignacion
from app.modelos.dispositivo import Dispositivo  # ✅ Importamos Dispositivo
from app.esquemas.ip_asignacion_esquemas import IpAsignacionCrear, IpAsignacionActualizar

def registrar_nueva_ip(mac_address: str, nueva_ip: str, db: Session):
    """
    Registra una nueva IP en la tabla ip_asignaciones para un dispositivo basado en su MAC.
    Si el dispositivo no existe, lanza un error.
    """
    # Buscar el dispositivo por su MAC
    dispositivo = db.query(Dispositivo).filter(Dispositivo.mac_address == mac_address).first()

    if not dispositivo:
        raise HTTPException(status_code=404, detail=f"Dispositivo con MAC {mac_address} no encontrado")

    print(f"[INFO] Registrando nueva IP {nueva_ip} para el dispositivo con MAC {mac_address}")

    # Crear un nuevo registro en ip_asignaciones
    nueva_asignacion = IpAsignacion(
        dispositivo_id=dispositivo.dispositivo_id,
        ip_address=nueva_ip
    )

    db.add(nueva_asignacion)
    # ❌ NO HACEMOS `db.commit()` aquí, porque ya hay una transacción activa.
    db.flush()  # ✅ `flush()` manda los cambios a la BD sin cerrar la transacción
    db.refresh(nueva_asignacion)  # Mantiene el objeto sincronizado

    return nueva_asignacion



def listar_ip_asignaciones(db: Session):
    """
    Retorna todas las IPs registradas en la base de datos.
    """
    return db.query(IpAsignacion).all()

def obtener_ultima_ip_dispositivo(db: Session, dispositivo_id: int):
    """
    Obtiene la última IP asignada a un dispositivo ordenando por fecha de creación.
    """
    ultima_ip = db.query(IpAsignacion.ip_address).filter(
        IpAsignacion.dispositivo_id == dispositivo_id
    ).order_by(IpAsignacion.fecha_creacion.desc()).first()

    return ultima_ip[0] if ultima_ip else None

def actualizar_ip_asignacion(ip_id: int, datos: IpAsignacionActualizar, db: Session):
    """
    Actualiza el estado de una IP en la base de datos.
    """
    ip_existente = db.query(IpAsignacion).filter(IpAsignacion.ip_asignacion_id == ip_id).first()
    
    if not ip_existente:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(ip_existente, key, value)
    
    db.commit()
    db.refresh(ip_existente)
    return ip_existente

def eliminar_ip_asignacion(ip_id: int, db: Session):
    """
    Elimina una IP asignada de la base de datos.
    """
    ip_existente = db.query(IpAsignacion).filter(IpAsignacion.ip_asignacion_id == ip_id).first()
    
    if not ip_existente:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    db.delete(ip_existente)
    db.commit()
    return {"message": "Registro eliminado exitosamente"}
