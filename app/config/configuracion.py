# 🔒 Configuración de seguridad
CLAVE_SECRETA = "-yH_d1ozKxGcqAevs5D4I6DaesQI5lziHIvDoJ1cX9k"
ALGORITMO = "HS256"
TIEMPO_EXPIRACION_TOKEN_MINUTOS = 1440  # 24 horas

# 📦 Configuración de la base de datos
URL_BASE_DATOS = "postgresql://jorgezumbamorales:Espoch1.@localhost:5432/web_app_db"

# 🌍 Configuraciones generales
MODO_DEPURACION = True

# 📧 Configuración del correo electrónico
SERVIDOR_CORREO = "smtp.gmail.com"
PUERTO_CORREO = 587
USUARIO_CORREO = "jorgezumba2000@gmail.com"  # Reemplaza con tu correo real
CONTRASENA_CORREO = "mjqw qwgt udef wqhy"  # Contraseña de aplicación generada
REMITENTE_CORREO = USUARIO_CORREO  # Usamos el mismo correo como remitente

# 🔮 Configuración de la API de Gemini
GEMINI_API_KEY = "AIzaSyD37HdnhWkJApLwJK86STk-sQqSMH_9MOU"
GEMINI_API_KEY_2 = "AIzaSyDoE9e6kOEvXGBO8uweoAKfNi099eNMUzE"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
