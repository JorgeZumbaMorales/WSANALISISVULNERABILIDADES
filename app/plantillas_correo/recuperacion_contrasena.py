def plantilla_recuperacion(codigo: str, usuario: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recuperación de Contraseña</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #F4F4F9;
                color: #4A4A4A;
                text-align: center;
                padding: 20px;
            }}
            .container {{
                background: white;
                max-width: 500px;
                margin: 0 auto;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background-color: #0A2342;
                color: white;
                padding: 10px;
                font-size: 20px;
                border-radius: 8px 8px 0 0;
            }}
            .codigo {{
                font-size: 24px;
                font-weight: bold;
                color: #ff3f00;
                background: #f8d7da;
                padding: 10px;
                border-radius: 5px;
                display: inline-block;
                margin: 10px 0;
            }}
            .footer {{
                font-size: 14px;
                color: #3E92CC;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">Recuperación de Contraseña</div>
            <p>Hola <strong>{usuario}</strong>,</p>
            <p>Hemos recibido una solicitud para restablecer tu contraseña.</p>
            <p>Por favor, usa el siguiente código para continuar con el proceso:</p>
            <p class="codigo">{codigo}</p>
            <p>Si no solicitaste este cambio, puedes ignorar este mensaje.</p>
            <p class="footer">Este código tiene una validez limitada.</p>
        </div>
    </body>
    </html>
    """
