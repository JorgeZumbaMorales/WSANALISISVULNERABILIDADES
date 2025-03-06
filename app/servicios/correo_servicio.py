import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config.configuracion import (
    SERVIDOR_CORREO, PUERTO_CORREO, USUARIO_CORREO, CONTRASENA_CORREO, REMITENTE_CORREO
)

class ServicioCorreo:
    @staticmethod
    def enviar_correo(destinatarios: list, asunto: str, mensaje: str, es_html=False):
        try:
            # 🔹 Configurar la conexión con Gmail
            servidor = smtplib.SMTP(SERVIDOR_CORREO, PUERTO_CORREO)
            servidor.starttls()  # Habilita la seguridad TLS
            servidor.login(USUARIO_CORREO, CONTRASENA_CORREO)

            # 🔹 Crear el correo
            correo = MIMEMultipart()
            correo["From"] = REMITENTE_CORREO
            correo["To"] = ", ".join(destinatarios)
            correo["Subject"] = asunto

            # 🔹 Agregar mensaje en HTML o texto plano
            if es_html:
                correo.attach(MIMEText(mensaje, "html"))
            else:
                correo.attach(MIMEText(mensaje, "plain"))

            # 🔹 Enviar correo
            servidor.sendmail(REMITENTE_CORREO, destinatarios, correo.as_string())
            servidor.quit()

            print(f"✅ Correo enviado a {destinatarios}")
            return {"estado": "exito", "mensaje": "Correo enviado correctamente"}

        except Exception as error:
            print(f"❌ Error al enviar el correo: {error}")
            return {"estado": "error", "mensaje": str(error)}
