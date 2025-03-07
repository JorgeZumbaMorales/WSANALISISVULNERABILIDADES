from sqlalchemy.orm import Session
from app.modelos.codigo_recuperacion import CodigoRecuperacion
from app.modelos.usuario import Usuario
from datetime import datetime
from fastapi import HTTPException
from datetime import datetime, timedelta
import bcrypt
from app.plantillas_correo import recuperacion_contrasena as plantilla_recuperacion
from app.servicios.correo_servicio import ServicioCorreo
class RecuperacionServicio:
    @staticmethod
    def generar_codigo() -> str:
        """Genera un código de 6 dígitos."""
        import random
        return str(random.randint(100000, 999999))

    @staticmethod
    def almacenar_codigo(db: Session, usuario_id: int, codigo: str):
        """Guarda o reemplaza un código de recuperación en la base de datos."""
        
        # 🗑 Eliminar código anterior si existe
        db.query(CodigoRecuperacion).filter(CodigoRecuperacion.usuario_id == usuario_id).delete()

        # 🛠 Encriptar código antes de almacenarlo
        codigo_hash = bcrypt.hashpw(codigo.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # 📌 Crear un nuevo registro de código de recuperación
        nuevo_codigo = CodigoRecuperacion(
            usuario_id=usuario_id,
            codigo_hash=codigo_hash,  # 🟢 CAMBIO AQUÍ
            fecha_expiracion=datetime.utcnow() + timedelta(minutes=10)  # Expira en 10 min
        )

        # 🔄 Guardar en la base de datos
        db.add(nuevo_codigo)
        db.commit()

    @staticmethod
    def enviar_codigo_recuperacion(db: Session, usuario_id: int, correo: str, usuario: str):
        """Genera un código, lo almacena en la BD y lo envía al usuario."""
        
        codigo = RecuperacionServicio.generar_codigo()
        
        # 🔹 Guardar el código en la BD directamente con el usuario_id
        RecuperacionServicio.almacenar_codigo(db, usuario_id, codigo)

        # 🔹 Generar el correo con la plantilla
        mensaje_html = plantilla_recuperacion.plantilla_recuperacion(codigo, usuario)

        return ServicioCorreo.enviar_correo(
            destinatarios=[correo],
            asunto="🔒 Código de Recuperación",
            mensaje=mensaje_html,
            es_html=True
        )


    @staticmethod
    def validar_codigo(db: Session, usuario: str, codigo_ingresado: str):
        """Verifica si el código ingresado es correcto y sigue activo."""
        usuario_obj = db.query(Usuario).filter(Usuario.nombre_usuario == usuario).first()
        if not usuario_obj:
            return {"estado": "error", "mensaje": "Usuario no encontrado."}

        codigo_obj = db.query(CodigoRecuperacion).filter(CodigoRecuperacion.usuario_id == usuario_obj.usuario_id).first()

        if not codigo_obj or codigo_obj.fecha_expiracion < datetime.utcnow():
            return {"estado": "error", "mensaje": "Código expirado o inexistente."}

        # 🔹 Comparar el código ingresado con el hash almacenado
        if not bcrypt.checkpw(codigo_ingresado.encode("utf-8"), codigo_obj.codigo_hash.encode("utf-8")):
            return {"estado": "error", "mensaje": "Código incorrecto."}

        return {"estado": "exito", "mensaje": "Código válido."}

    @staticmethod
    def actualizar_contrasena(db: Session, usuario: str, nueva_contrasena: str):
        """Actualiza la contraseña si el código fue validado."""
        usuario_obj = db.query(Usuario).filter(Usuario.nombre_usuario == usuario).first()
        if not usuario_obj:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")

        # Hashear la nueva contraseña
        salt = bcrypt.gensalt()
        usuario_obj.contrasena = bcrypt.hashpw(nueva_contrasena.encode("utf-8"), salt).decode("utf-8")

        db.commit()

        # Eliminar código usado
        db.query(CodigoRecuperacion).filter(CodigoRecuperacion.usuario_id == usuario_obj.usuario_id).delete()
        db.commit()

        return {"message": "Contraseña actualizada correctamente."}
