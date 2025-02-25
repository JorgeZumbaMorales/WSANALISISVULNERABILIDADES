from sqlalchemy.orm import Session
from app.modelos.dispositivo import Dispositivo
from app.modelos.ip_asignaciones import IpAsignacion
from app.esquemas.dispositivo_esquemas import DispositivoCrear, DispositivoActualizar, IpAsignacionCrear
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_dispositivo(datos_dispositivo: DispositivoCrear, db: Session):
    # Verificar si la MAC ya existe
    dispositivo_existente = db.query(Dispositivo).filter(Dispositivo.mac_address == datos_dispositivo.mac_address).first()
    if dispositivo_existente:
        return excepcion_no_encontrado("Ya existe un dispositivo con esta MAC")

    nuevo_dispositivo = Dispositivo(
        nombre_dispositivo=datos_dispositivo.nombre_dispositivo,
        mac_address=datos_dispositivo.mac_address,
        fabricante=datos_dispositivo.fabricante
    )
    db.add(nuevo_dispositivo)
    db.commit()
    db.refresh(nuevo_dispositivo)

    # Crear asignación de IP
    nueva_ip = IpAsignacion(
        dispositivo_id=nuevo_dispositivo.dispositivo_id,
        ip_address=datos_dispositivo.ip_address
    )
    db.add(nueva_ip)
    db.commit()

    return nuevo_dispositivo

def listar_dispositivos(db: Session):
    dispositivos = db.query(Dispositivo).all()
    dispositivos_con_ips = []
    
    for dispositivo in dispositivos:
        ips = [ip.ip_address for ip in db.query(IpAsignacion).filter(IpAsignacion.dispositivo_id == dispositivo.dispositivo_id).all()]
        dispositivos_con_ips.append({
            "dispositivo_id": dispositivo.dispositivo_id,
            "nombre_dispositivo": dispositivo.nombre_dispositivo,
            "mac_address": dispositivo.mac_address,
            "fabricante": dispositivo.fabricante,
            "ips": ips
        })

    return dispositivos_con_ips

def asignar_ip(datos_ip: IpAsignacionCrear, db: Session):
    nueva_ip = IpAsignacion(
        dispositivo_id=datos_ip.dispositivo_id,
        ip_address=datos_ip.ip_address
    )
    db.add(nueva_ip)
    db.commit()
    return respuesta_exitosa("IP asignada correctamente")

def obtener_historial_ips(dispositivo_id: int, db: Session):
    ips = db.query(IpAsignacion).filter(IpAsignacion.dispositivo_id == dispositivo_id).all()
    return [ip.ip_address for ip in ips]
