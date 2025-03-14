import requests
import time
from fastapi import HTTPException
from app.config.configuracion import GEMINI_API_KEY, GEMINI_URL

def generar_respuesta_gemini(prompt: str, max_retries=3):
    """📌 Enviar una solicitud a la API de Gemini con reintentos en caso de error 429."""
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="La API Key de Gemini no está configurada.")

    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    for intento in range(1, max_retries + 1):
        try:
            response = requests.post(GEMINI_URL, json=data, headers=headers)
            response.raise_for_status()
            resultado = response.json()

            # Extraer la respuesta generada por la IA
            return resultado.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sin respuesta")

        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                espera = 5 * intento  # 🔄 Espera progresiva: 5s, 10s, 15s...
                print(f"[WARN] Error 429: Too Many Requests. Reintentando en {espera} segundos...")
                time.sleep(espera)
            else:
                raise HTTPException(status_code=500, detail=f"Error al conectar con Gemini: {str(e)}")

    raise HTTPException(status_code=500, detail="No se pudo obtener respuesta de Gemini tras varios intentos.")



def analizar_riesgo_ia(puertos):
    """
    🔥 Analiza el nivel de riesgo de un dispositivo basado en sus puertos abiertos.
    """
    if not puertos:
        return "Sin Riesgo"

    # Formateamos la lista de puertos abiertos para el prompt
    lista_puertos = ", ".join(f"{p.puerto} ({p.servicio})" for p in puertos)
    
    prompt = (
        f"Tengo un dispositivo con los siguientes puertos abiertos: {lista_puertos}. "
        "¿Qué nivel de riesgo representa este dispositivo? Responde SOLO con: Alto, Medio, Bajo o Sin Riesgo."
    )

    # Enviar el prompt a Gemini y obtener la evaluación
    respuesta_ia = generar_respuesta_gemini(prompt).strip()

    # Verificar si la respuesta es válida
    if respuesta_ia in {"Alto", "Medio", "Bajo", "Sin Riesgo"}:
        return respuesta_ia
    else:
        return "Bajo"  # En caso de que Gemini no devuelva una respuesta válida, se asume riesgo bajo.
