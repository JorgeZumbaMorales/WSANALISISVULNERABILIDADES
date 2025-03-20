from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.configuracion_escaneo import ConfiguracionEscaneo
from app.modelos.configuracion_horas_escaneo import ConfiguracionHorasEscaneo
from app.esquemas.configuracion_escaneos_esquemas import ConfiguracionEscaneoCrear


def crear_configuracion_escaneo_con_horas(datos: ConfiguracionEscaneoCrear, horas: list[str], db: Session):
    try:
        if datos.estado:  # ✅ Desactivar anteriores si la nueva es activa
            db.query(ConfiguracionEscaneo).filter(ConfiguracionEscaneo.estado == True).update({"estado": False})

        # 🔹 1️⃣ Crear la configuración principal en `configuracion_escaneo`
        nueva_configuracion = ConfiguracionEscaneo(
            nombre_configuracion_escaneo=datos.nombre_configuracion_escaneo,
            tipo_escaneo_id=datos.tipo_escaneo_id,
            frecuencia_minutos=None,  # ❌ No se usa en escaneo por horas
            fecha_inicio=datos.fecha_inicio,
            fecha_fin=datos.fecha_fin,
            estado=datos.estado if datos.estado is not None else False
        )
        db.add(nueva_configuracion)
        db.flush()  # 💾 Guardar temporalmente para obtener el ID antes del commit

        # 🔹 2️⃣ Insertar las horas en `configuracion_horas_escaneo`
        for hora in horas:
            nueva_hora = ConfiguracionHorasEscaneo(
                configuracion_escaneo_id=nueva_configuracion.configuracion_escaneo_id,
                hora=hora
            )
            db.add(nueva_hora)

        # 🔹 3️⃣ Confirmar la transacción
        db.commit()
        db.refresh(nueva_configuracion)

        return {
            "mensaje": "Configuración de escaneo creada exitosamente",
            "data": nueva_configuracion
        }

    except Exception as e:
        db.rollback()  # 🚨 Revertir cambios si hay error
        raise HTTPException(status_code=500, detail=f"Error al crear la configuración: {str(e)}")
