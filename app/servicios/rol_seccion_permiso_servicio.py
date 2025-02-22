from sqlalchemy.orm import Session
from app.modelos.rol_seccion_permiso import RolSeccionPermiso
from app.esquemas.rol_seccion_permiso_esquemas import RolSeccionPermisoCrear, RolSeccionPermisoActualizar
from fastapi import HTTPException

def crear_rol_seccion_permiso(datos: RolSeccionPermisoCrear, db: Session):
    nuevo_registro = RolSeccionPermiso(
        rol_id=datos.rol_id,
        seccion_id=datos.seccion_id,
        permiso_id=datos.permiso_id,
        estado=datos.estado
    )
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return nuevo_registro

def listar_rol_seccion_permisos(db: Session):
    return db.query(RolSeccionPermiso).all()

def actualizar_estado_rol_seccion_permiso(rol_seccion_permiso_id: int, datos: RolSeccionPermisoActualizar, db: Session):
    registro = db.query(RolSeccionPermiso).filter(RolSeccionPermiso.rol_seccion_permiso_id == rol_seccion_permiso_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    if datos.estado is not None:
        registro.estado = datos.estado

    db.commit()
    db.refresh(registro)
    return registro

def eliminar_rol_seccion_permiso(rol_seccion_permiso_id: int, db: Session):
    registro = db.query(RolSeccionPermiso).filter(RolSeccionPermiso.rol_seccion_permiso_id == rol_seccion_permiso_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    db.delete(registro)
    db.commit()
    return {"message": "Registro eliminado exitosamente"}
