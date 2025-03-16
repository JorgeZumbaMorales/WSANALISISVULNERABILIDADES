from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.rutas.ruta_usuario import router as usuarios_router
from app.rutas.ruta_rol import router as roles_router
from app.rutas.ruta_permiso import router as permisos_router
from app.rutas.ruta_rol_seccion_permiso import router as ruta_rol_seccion_permiso
from app.rutas.ruta_rol_usuario import router as rol_usuario_router
from app.rutas.ruta_dispositivo import router as dispositivo_router
from app.rutas.ruta_categoria import router as categoria_router
from app.rutas.ruta_vulnerabilidad import router as vulnerabilidad_router
from app.rutas.ruta_historial_vulnerabilidad import router as historial_vulnerabilidad_router
from app.rutas.ruta_tipo_alerta import router as tipo_alerta_router
from app.rutas.ruta_canal_alerta import router as canal_alerta_router
from app.rutas.ruta_notificacion import router as notificacion_router
from app.rutas.ruta_tipo_reporte import router as tipo_reporte_router
from app.rutas.ruta_reporte_generado import router as reporte_generado_router
from app.rutas.ruta_seccion import router as seccion_router
from app.rutas.ruta_puerto_abierto import router as puerto_abierto_router
from app.rutas.ruta_sistema_operativo import router as sistema_operativo_router
from app.rutas.ruta_autenticacion import router as autenticacion_router
from app.rutas.ruta_correo import router as correo_router 
from app.rutas.ruta_recuperacion_contrasena import router as recuperacion_contrasena_router
from app.rutas.ruta_configuracion_escaneo import router as configuracion_escaneo_router
from app.rutas.ruta_tipos_escaneo import router as tipo_escaneo_router
from app.rutas.ruta_riesgo import router as riesgo_router
from app.rutas.ruta_dispositivo_riesgo import router as dispositivo_riesgo_router
from app.rutas.ruta_recomendacion_puerto import router as recomendacion_puerto_router
from app.rutas.ruta_generar_recomendaciones import router as generar_recomendaciones_router
app = FastAPI(
    title="API de Gestión y Seguridad",
    description="Esta API gestiona usuarios, dispositivos, vulnerabilidades y más.",
    version="1.0.0"
)


app.include_router(usuarios_router)
app.include_router(roles_router)
app.include_router(permisos_router)
app.include_router(ruta_rol_seccion_permiso)
app.include_router(rol_usuario_router)
app.include_router(dispositivo_router)
app.include_router(categoria_router)
app.include_router(vulnerabilidad_router)
app.include_router(historial_vulnerabilidad_router)
app.include_router(tipo_alerta_router)
app.include_router(canal_alerta_router)
app.include_router(notificacion_router)
app.include_router(tipo_reporte_router)
app.include_router(reporte_generado_router)
app.include_router(seccion_router)
app.include_router(puerto_abierto_router)
app.include_router(sistema_operativo_router)
app.include_router(autenticacion_router)
app.include_router(correo_router)
app.include_router(recuperacion_contrasena_router)
app.include_router(configuracion_escaneo_router)
app.include_router(tipo_escaneo_router)
app.include_router(riesgo_router)
app.include_router(dispositivo_riesgo_router)
app.include_router(recomendacion_puerto_router)
app.include_router(generar_recomendaciones_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido a la API!"}
