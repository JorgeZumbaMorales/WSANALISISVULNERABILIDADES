from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.servicios.dispositivo_servicio import actualizar_dispositivo
from app.modelos.dispositivo_sistema_operativo import DispositivoSistemaOperativo
from app.esquemas.dispositivo_esquemas import DispositivoActualizar

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
            DispositivoSistemaOperativo.estado == True
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
