from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.servicios.configuracion_escaneos_servicio import (
    crear_configuracion_escaneo, obtener_configuracion_escaneo,
    actualizar_configuracion_escaneo, listar_configuraciones_escaneo,
    eliminar_configuracion_escaneo, activar_configuracion_escaneo, listar_configuraciones_frecuencia,
    listar_configuraciones_horas
)
from app.esquemas.configuracion_escaneos_esquemas import (
    ConfiguracionEscaneoCrear, ConfiguracionEscaneoActualizar, ConfiguracionEscaneoActualizarEstado
)
from app.transacciones.transaccion_configuracion_escaneos import crear_configuracion_escaneo_con_horas
router = APIRouter(
    prefix="/configuracion_escaneos",
    tags=["Configuración de Escaneos"]
)

## ✅ 1️⃣ CREAR UNA NUEVA CONFIGURACIÓN DE ESCANEO
@router.post("/crear_configuracion_escaneo")
def crear_configuracion_escaneo_endpoint(
    datos: dict,  # 🔹 Recibir como dict para extraer manualmente
    db: Session = Depends(obtener_bd)
):
    try:
        # 🔹 Extraer horas si existen
        horas = datos.pop("horas", [])  

        # 🔹 Convertir los datos a Pydantic sin incluir `horas`
        config_datos = ConfiguracionEscaneoCrear(**datos)

        if config_datos.tipo_escaneo_id == 1:
            # 🔹 Guardar configuración de frecuencia
            resultado = crear_configuracion_escaneo(config_datos, db)
        elif config_datos.tipo_escaneo_id == 2:
            # 🔹 Guardar configuración con horas
            resultado = crear_configuracion_escaneo_con_horas(config_datos, horas, db)
        else:
            raise HTTPException(status_code=400, detail="Tipo de escaneo no válido")

        return {"mensaje": "Configuración creada exitosamente", "data": resultado}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la configuración: {str(e)}")

## ✅ 2️⃣ OBTENER UNA CONFIGURACIÓN DE ESCANEO POR ID
@router.get("/obtener_configuracion_escaneo/{configuracion_id}")
def obtener_configuracion_escaneo_endpoint(configuracion_id: int, db: Session = Depends(obtener_bd)):
    resultado = obtener_configuracion_escaneo(configuracion_id, db)
    return {"mensaje": "Configuración de escaneo obtenida exitosamente", "data": resultado}

## ✅ 3️⃣ ACTUALIZAR UNA CONFIGURACIÓN DE ESCANEO
@router.put("/actualizar_configuracion_escaneo/{configuracion_id}")
def actualizar_configuracion_escaneo_endpoint(configuracion_id: int, datos: ConfiguracionEscaneoActualizar, db: Session = Depends(obtener_bd)):
    resultado = actualizar_configuracion_escaneo(configuracion_id, datos, db)
    return {"mensaje": "Configuración de escaneo actualizada exitosamente", "data": resultado}

## ✅ 4️⃣ ACTIVAR UNA CONFIGURACIÓN DE ESCANEO
@router.put("/activar_configuracion/{configuracion_id}")
def activar_configuracion_endpoint(configuracion_id: int, db: Session = Depends(obtener_bd)):
    resultado = activar_configuracion_escaneo(configuracion_id, db)
    return {"mensaje": "Configuración de escaneo activada exitosamente", "data": resultado}

## ✅ 5️⃣ LISTAR TODAS LAS CONFIGURACIONES
@router.get("/listar_configuraciones_escaneo")
def listar_configuraciones_escaneo_endpoint(db: Session = Depends(obtener_bd)):
    resultado = listar_configuraciones_escaneo(db)
    return {"mensaje": "Lista de configuraciones de escaneo obtenida exitosamente", "data": resultado}

## ✅ 6️⃣ ELIMINAR UNA CONFIGURACIÓN DE ESCANEO
@router.delete("/eliminar_configuracion_escaneo/{configuracion_id}")
def eliminar_configuracion_escaneo_endpoint(configuracion_id: int, db: Session = Depends(obtener_bd)):
    resultado = eliminar_configuracion_escaneo(configuracion_id, db)
    return {"mensaje": "Configuración de escaneo eliminada exitosamente"}

## ✅ 1️⃣ LISTAR CONFIGURACIONES DE FRECUENCIA
@router.get("/listar_configuraciones_frecuencia")
def listar_configuraciones_frecuencia_endpoint(db: Session = Depends(obtener_bd)):
    resultado = listar_configuraciones_frecuencia(db)
    return {"mensaje": "Lista de configuraciones de escaneo por frecuencia obtenida exitosamente", "data": resultado}

## ✅ 2️⃣ LISTAR CONFIGURACIONES POR HORAS
@router.get("/listar_configuraciones_horas")
def listar_configuraciones_horas_endpoint(db: Session = Depends(obtener_bd)):
    resultado = listar_configuraciones_horas(db)
    return {"mensaje": "Lista de configuraciones de escaneo por horas obtenida exitosamente", "data": resultado}

