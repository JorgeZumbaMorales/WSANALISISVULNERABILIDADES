from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.servicios.dispositivo_servicio import actualizar_dispositivo
from app.esquemas.dispositivo_esquemas import DispositivoActualizar

from app.modelos.dispositivo import Dispositivo
from app.modelos.dispositivo_riesgo import DispositivoRiesgo
from app.modelos.dispositivo_sistema_operativo import DispositivoSistemaOperativo
from app.modelos.ip_asignaciones import IpAsignacion
from app.modelos.puerto_abierto import PuertoAbierto
from app.modelos.recomendacion_puerto import RecomendacionPuerto



def transaccion_actualizar_dispositivo_con_so(dispositivo_id: int, datos_dispositivo: dict, db: Session):
    try:
        nuevo_nombre = datos_dispositivo.nuevo_nombre
        nuevo_so_id = datos_dispositivo.nuevo_sistema_operativo_id

        if not nuevo_so_id:
            raise HTTPException(status_code=400, detail="Debe proporcionar un nuevo ID de sistema operativo")

        # ✅ 1. Actualizar nombre del dispositivo
        if nuevo_nombre:
            datos_nombre = DispositivoActualizar(nombre_dispositivo=nuevo_nombre)
            actualizar_dispositivo(dispositivo_id, datos_nombre, db)

        # ✅ 2. Buscar relación activa actual
        relacion = db.query(DispositivoSistemaOperativo).filter(
            DispositivoSistemaOperativo.dispositivo_id == dispositivo_id,

        ).first()

        if not relacion:
            raise HTTPException(status_code=404, detail="Relación activa del sistema operativo no encontrada")

        # ✅ 3. Actualizar solo el ID del sistema operativo
        relacion.sistema_operativo_id = nuevo_so_id
        db.commit()
        db.refresh(relacion)

        return {
            "dispositivo_id": dispositivo_id,
            "nuevo_nombre": nuevo_nombre,
            "nuevo_sistema_operativo_id": nuevo_so_id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en la transacción: {str(e)}")



def transaccion_eliminar_dispositivo_completo(dispositivo_id: int, db: Session):
    try:
        # 1. Eliminar recomendaciones de los puertos asociados al dispositivo
        puertos = db.query(PuertoAbierto).filter(PuertoAbierto.dispositivo_id == dispositivo_id).all()
        for puerto in puertos:
            db.query(RecomendacionPuerto).filter(RecomendacionPuerto.puerto_id == puerto.puerto_id).delete(synchronize_session=False)

        # 2. Eliminar puertos
        db.query(PuertoAbierto).filter(PuertoAbierto.dispositivo_id == dispositivo_id).delete(synchronize_session=False)

        # 3. Eliminar asignaciones IP
        db.query(IpAsignacion).filter(IpAsignacion.dispositivo_id == dispositivo_id).delete(synchronize_session=False)

        # 4. Eliminar relaciones con sistema operativo
        db.query(DispositivoSistemaOperativo).filter(DispositivoSistemaOperativo.dispositivo_id == dispositivo_id).delete(synchronize_session=False)

        # 5. Eliminar relaciones con riesgos
        db.query(DispositivoRiesgo).filter(DispositivoRiesgo.dispositivo_id == dispositivo_id).delete(synchronize_session=False)

        # 6. Eliminar el dispositivo
        dispositivo = db.query(Dispositivo).filter(Dispositivo.dispositivo_id == dispositivo_id).first()
        if not dispositivo:
            raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

        db.delete(dispositivo)
        db.commit()

        return {"message": "Dispositivo eliminado correctamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")


