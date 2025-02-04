from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.rutas.ruta_usuario import router as usuarios_router
from app.rutas.ruta_rol import router as roles_router
from app.rutas.ruta_permiso import router as permisos_router
from app.rutas.ruta_rol_permiso import router as rol_permiso_router
from app.rutas.ruta_rol_usuario import router as rol_usuario_router
from app.rutas.ruta_dispositivo import router as dispositivo_router
from app.rutas.ruta_categoria import router as categoria_router
from app.rutas.ruta_dispositivo_categoria import router as dispositivo_categoria_router
from app.rutas.ruta_vulnerabilidad import router as vulnerabilidad_router
from app.rutas.ruta_historial_vulnerabilidad import router as historial_vulnerabilidad_router
from app.rutas.ruta_tipo_alerta import router as tipo_alerta_router
from app.rutas.ruta_canal_alerta import router as canal_alerta_router
from app.rutas.ruta_notificacion import router as notificacion_router
from app.rutas.ruta_tipo_reporte import router as tipo_reporte_router
from app.rutas.ruta_reporte_generado import router as reporte_generado_router
from app.rutas.ruta_politica import router as politica_router
from app.rutas.ruta_regla import router as regla_router
from app.rutas.ruta_politica_regla import router as politica_regla_router
from app.rutas.ruta_herramienta import router as herramienta_router
from app.rutas.ruta_parametro import router as parametro_router
from app.rutas.ruta_herramienta_parametro import router as herramienta_parametro_router

app = FastAPI(
    title="API de Gestión y Seguridad",
    description="Esta API gestiona usuarios, dispositivos, vulnerabilidades y más.",
    version="1.0.0"
)


app.include_router(usuarios_router)
app.include_router(roles_router)
app.include_router(permisos_router)
app.include_router(rol_permiso_router)
app.include_router(rol_usuario_router)
app.include_router(dispositivo_router)
app.include_router(categoria_router)
app.include_router(dispositivo_categoria_router)
app.include_router(vulnerabilidad_router)
app.include_router(historial_vulnerabilidad_router)
app.include_router(tipo_alerta_router)
app.include_router(canal_alerta_router)
app.include_router(notificacion_router)
app.include_router(tipo_reporte_router)
app.include_router(reporte_generado_router)
app.include_router(politica_router)
app.include_router(regla_router)
app.include_router(politica_regla_router)
app.include_router(herramienta_router)
app.include_router(parametro_router)
app.include_router(herramienta_parametro_router)

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
