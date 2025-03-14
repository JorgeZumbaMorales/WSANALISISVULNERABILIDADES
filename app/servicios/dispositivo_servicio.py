from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from app.modelos.dispositivo import Dispositivo
from app.esquemas.dispositivo_esquemas import DispositivoCrear, DispositivoActualizar, DispositivoActualizarEstado
from app.modelos.dispositivo_sistema_operativo import DispositivoSistemaOperativo
from app.modelos.sistema_operativo import SistemaOperativo
from app.modelos.ip_asignaciones import IpAsignacion

def crear_dispositivo(datos_dispositivo: DispositivoCrear, db: Session):
    print(f"[DEBUG] Tipo de db en crear_dispositivo: {type(db)}")
    dispositivo_existente = db.query(Dispositivo).filter(Dispositivo.mac_address == datos_dispositivo.mac_address).first()
    if dispositivo_existente:
        raise HTTPException(status_code=400, detail="Ya existe un dispositivo con esta MAC")
    
    nuevo_dispositivo = Dispositivo(
        nombre_dispositivo=datos_dispositivo.nombre_dispositivo,
        mac_address=datos_dispositivo.mac_address
    )
    db.add(nuevo_dispositivo)
    db.flush() 
    db.refresh(nuevo_dispositivo)
    return nuevo_dispositivo

def listar_dispositivos(db: Session):
    print(f"[DEBUG] Tipo de db en crear_dispositivo: {type(db)}")
    return db.query(Dispositivo).all()

def listar_dispositivos_completo(db: Session):
    print(f"[DEBUG] Tipo de db en listar_dispositivos_completo: {type(db)}")

    """
    Obtiene la lista de dispositivos con estado True, su sistema operativo y la última IP asignada.
    """
    dispositivos = db.query(Dispositivo).filter(Dispositivo.estado == True).all()  # 🔥 Solo dispositivos activos

    dispositivos_resultado = []
    for dispositivo in dispositivos:
        # Obtener el sistema operativo si existe
        if dispositivo.sistema_operativo_relacion:
            primer_so = dispositivo.sistema_operativo_relacion[0]  # ✅ Acceder al primer SO si existe
            so = primer_so.sistema_operativo.nombre_so
        else:
            so = "Desconocido"

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
            "estado": dispositivo.estado  # ✅ Siempre será True por el filtro, pero se mantiene por claridad
        })

    return dispositivos_resultado

def listar_todos_los_dispositivos_completo(db: Session):
    print(f"[DEBUG] Tipo de db en listar_todos_los_dispositivos_completo: {type(db)}")

    """
    Obtiene la lista de TODOS los dispositivos, su sistema operativo y la última IP asignada.
    """
    dispositivos = db.query(Dispositivo).all()  # 🔥 Ahora obtiene TODOS los dispositivos

    dispositivos_resultado = []
    for dispositivo in dispositivos:
        # Obtener el sistema operativo si existe
        if dispositivo.sistema_operativo_relacion:
            primer_so = dispositivo.sistema_operativo_relacion[0]  # ✅ Acceder al primer SO si existe
            so = primer_so.sistema_operativo.nombre_so
        else:
            so = "Desconocido"

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
            "estado": dispositivo.estado  # ✅ Puede ser True o False
        })

    return dispositivos_resultado


def obtener_dispositivo_por_mac(db: Session, mac_address: str):
    print(f"[DEBUG] Tipo de db en crear_dispositivo: {type(db)}")

    """
    Busca un dispositivo por su dirección MAC.
    """
    return db.query(Dispositivo).filter(Dispositivo.mac_address == mac_address).first()


def actualizar_dispositivo(dispositivo_id: int, datos_dispositivo: DispositivoActualizar, db: Session):
    print(f"[DEBUG] Tipo de db en crear_dispositivo: {type(db)}")

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
 

def actualizar_estado_dispositivo(dispositivo_id: int, datos_estado: DispositivoActualizarEstado, db: Session):
    """
    Actualiza únicamente el estado de un dispositivo en la base de datos.
    """
    print(f"[DEBUG] Actualizando estado del dispositivo {dispositivo_id} a {datos_estado.estado}")

    dispositivo_existente = db.query(Dispositivo).filter(Dispositivo.dispositivo_id == dispositivo_id).first()

    if not dispositivo_existente:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    dispositivo_existente.estado = datos_estado.estado  # ✅ Se usa la validación del esquema

    db.commit()
    db.flush() 
    db.refresh(dispositivo_existente)
    
    print(f"[INFO] Estado del dispositivo {dispositivo_id} actualizado a {datos_estado.estado}")
    return dispositivo_existente


