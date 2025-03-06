from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.dispositivo_sistema_operativo import DispositivoSistemaOperativo
from app.esquemas.dispositivo_sistema_operativo_esquemas import DispositivoSistemaOperativoCrear, DispositivoSistemaOperativoActualizar

def crear_dispositivo_sistema_operativo(datos: DispositivoSistemaOperativoCrear, db: Session):
    nuevo_registro = DispositivoSistemaOperativo(
        dispositivo_id=datos.dispositivo_id,
        sistema_operativo_id=datos.sistema_operativo_id,
        estado=datos.estado
    )
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return nuevo_registro

def listar_dispositivos_sistemas_operativos(db: Session):
    return db.query(DispositivoSistemaOperativo).all()

def actualizar_dispositivo_sistema_operativo(dispositivo_so_id: int, datos: DispositivoSistemaOperativoActualizar, db: Session):
    registro_existente = db.query(DispositivoSistemaOperativo).filter(DispositivoSistemaOperativo.dispositivo_so_id == dispositivo_so_id).first()
    if not registro_existente:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(registro_existente, key, value)
    
    db.commit()
    db.refresh(registro_existente)
    return registro_existente

def eliminar_dispositivo_sistema_operativo(dispositivo_so_id: int, db: Session):
    registro_existente = db.query(DispositivoSistemaOperativo).filter(DispositivoSistemaOperativo.dispositivo_so_id == dispositivo_so_id).first()
    if not registro_existente:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    db.delete(registro_existente)
    db.commit()
    return {"message": "Registro eliminado exitosamente"}
