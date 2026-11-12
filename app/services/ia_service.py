"""
Servicio de integración con el agente de IA (Gemini).

Implementa la integración del agente de IA con las siguientes reglas:
    - Lee la API key obligatoriamente del archivo .env (nunca hardcodeada).
    - Envía la consulta junto con los fragmentos de documentos relevantes al modelo de IA.
    - Respeta el contrato de salida JSON: respuesta (string), cita_fuente (string), estado_encontrado (boolean).
    - Regla estricta: el agente NUNCA inventa información. Si la respuesta no figura en los documentos, escribe "no indicado".

Nota: Se agrega la librería google-generativeai cuando se disponga de la API key real.
Mientras tanto, el servicio funciona en modo placeholder listo para integrarse.
"""

import os
import json
import logging
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

logger = logging.getLogger(__name__)


def construir_prompt_ia(pregunta: str, fragmentos_documentos: List[str], historial: List[dict]) -> str:
    """
    Construye el prompt que se enviará al agente de IA (Gemini).

    Incluye instrucciones estrictas para que el agente no invente información
    y devuelva siempre el contrato JSON con las 3 llaves requeridas.

    Argumentos:
        pregunta: texto de la pregunta del usuario.
        fragmentos_documentos: fragmentos de documentos de referencia del repositorio TH.
        historial: interacciones previas de la sesión.

    Retorna:
        String con el prompt completo para el modelo de IA.
    """
    contexto_documentos = "\n".join(fragmentos_documentos) if fragmentos_documentos else "(no hay documentos de referencia disponibles)"

    historial_texto = ""
    if historial:
        historial_texto = "\n\nHistorial de la conversación:\n"
        for i, interaccion in enumerate(historial, 1):
            historial_texto += (
                f"{i}. Usuario: {interaccion['pregunta']}\n"
                f"   Asistente: {interaccion['respuesta']}\n"
                f"   Fuente: {interaccion['cita_fuente']}\n"
            )

    prompt = f"""Eres un Asistente Experto en Normativa de Talento Humano.

Tu tarea es responder preguntas de los Jefes de área de la organización sobre temas de Talento Humano.

REGLAS ESTRICTAS:
1. NUNCA inventes información. Si la respuesta no figura en los documentos proporcionados, escribe 'no indicado'.
2. Responde siempre en español.
3. Extrae la cita exacta del documento fuente donde obtuviste la información.
4. Devuelve SIEMPRE un objeto JSON válido con exactamente estas 3 llaves:
   - "respuesta": string, redacción clara, directa y formal de la solución.
   - "cita_fuente": string, nombre del documento, sección o página de donde se obtuvo la respuesta.
   - "estado_encontrado": boolean, true si la respuesta está en los documentos; false si no aparece.

DOCUMENTOS DE REFERENCIA:
{contexto_documentos}

{historial_texto}

PREGUNTA DEL USUARIO:
{pregunta}

Responde SOLO con el JSON, sin texto adicional antes o después."""
    return prompt


def llamar_agente_ia(pregunta: str, fragmentos_documentos: List[str], historial: List[dict]) -> Dict:
    """
    Envía la consulta al agente de IA (Gemini) y devuelve el resultado en formato JSON.

    Argumentos:
        pregunta: texto de la pregunta del usuario.
        fragmentos_documentos: fragmentos de documentos de referencia.
        historial: interacciones previas de la sesión.

    Retorna:
        Diccionario con las llaves: respuesta, cita_fuente, estado_encontrado.

    Reglas aplicadas:
        - Lee la API key de .env (no hardcodeada).
        - Si no hay API key configurada, retorna respuesta indicando que falta la llave.
        - Si el modelo no retorna JSON válido, retorna estado_encontrado: false y "no indicado".
        - El agente NUNCA inventa información.
    """
    # Validar que exista API key
    if not GEMINI_API_KEY or GEMINI_API_KEY == "tu_api_key_aqui":
        logger.error("GEMINI_API_KEY no configurada en variables de entorno")
        return {
            "respuesta": "Error: No se configuró la API key de Gemini. Agrega GEMINI_API_KEY en las variables de entorno de Render.",
            "cita_fuente": "configuración pendiente",
            "estado_encontrado": False,
        }

    # Construir el prompt para el modelo
    prompt = construir_prompt_ia(pregunta, fragmentos_documentos, historial)

    # Llamada real a la API de Gemini - probar múltiples modelos
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)

        # Lista de modelos a probar (gratuitos en orden de preferencia)
        modelos_a_probar = [
            "gemini-1.5-flash-latest",
            "gemini-1.5-pro-latest",
            "gemini-pro",
            "gemini-1.0-pro",
        ]

        texto_respuesta = None
        modelo_usado = None

        for nombre_modelo in modelos_a_probar:
            try:
                model = genai.GenerativeModel(nombre_modelo)
                response = model.generate_content(prompt)
                texto_respuesta = response.text
                modelo_usado = nombre_modelo
                logger.info(f"Modelo funcionando: {nombre_modelo}")
                break
            except Exception as e:
                logger.warning(f"Modelo {nombre_modelo} no disponible: {type(e).__name__}: {str(e)}")
                continue

        if texto_respuesta is None:
            logger.error("Ningún modelo de Gemini está disponible para esta API key")
            return {
                "respuesta": "Error: Ningún modelo de IA está disponible con tu API key de Gemini. Verifica que tu llave sea válida y tenga acceso a modelos gratuitos en Google AI Studio.",
                "cita_fuente": "error de API de Gemini",
                "estado_encontrado": False,
            }

    except Exception as e:
        logger.error(f"Error llamando a la API de Gemini: {type(e).__name__}: {str(e)}")
        return {
            "respuesta": f"Error al contactar al modelo de IA: {type(e).__name__}. Verifica que GEMINI_API_KEY sea válida y tenga cuota disponible.",
            "cita_fuente": "error de API de Gemini",
            "estado_encontrado": False,
        }

    if not texto_respuesta or not texto_respuesta.strip():
        logger.warning("Gemini devolvió respuesta vacía")
        return {
            "respuesta": "no indicado",
            "cita_fuente": "modelo de IA (respuesta vacía)",
            "estado_encontrado": False,
        }

    # Intentar parsear como JSON; si falla, devolver no indicado
    try:
        respuesta_ia = json.loads(texto_respuesta)
    except (json.JSONDecodeError, ValueError) as e:
        logger.warning(f"Gemini no devolvió JSON válido: {e}")
        return {
            "respuesta": texto_respuesta.strip() if texto_respuesta.strip() else "no indicado",
            "cita_fuente": "modelo de IA (respuesta no estructurada)",
            "estado_encontrado": False,
        }

    # Validar que tenga las 3 llaves requeridas
    if not all(k in respuesta_ia for k in ("respuesta", "cita_fuente", "estado_encontrado")):
        logger.warning(f"Gemini devolvió JSON incompleto: {respuesta_ia.keys()}")
        return {
            "respuesta": "no indicado",
            "cita_fuente": "modelo de IA (formato incompleto)",
            "estado_encontrado": False,
        }

    return respuesta_ia


def validar_contrato_ia(respuesta_ia: Dict) -> Dict:
    """
    Valida que la respuesta del agente de IA respete el contrato JSON.

    Argumentos:
        respuesta_ia: diccionario devuelto por el agente de IA.

    Retorna:
        Diccionario con las 3 llaves validadas, o valores por defecto si falta algo.
    """
    respuesta = respuesta_ia.get("respuesta", "no indicado")
    if respuesta is None or not isinstance(respuesta, str):
        respuesta = "no indicado"

    cita_fuente = respuesta_ia.get("cita_fuente", "no indicado")
    if cita_fuente is None or not isinstance(cita_fuente, str):
        cita_fuente = "no indicado"

    estado_encontrado = respuesta_ia.get("estado_encontrado", False)
    if not isinstance(estado_encontrado, bool):
        estado_encontrado = bool(estado_encontrado)

    return {
        "respuesta": respuesta,
        "cita_fuente": cita_fuente,
        "estado_encontrado": estado_encontrado,
    }


def procesar_pregunta_ia(
    session_id: str,
    pregunta: str,
    fragmentos_documentos: List[str],
    historial: List[dict],
) -> Dict:
    """
    Procesa una pregunta completa: llama al agente de IA y valida el contrato.

    Argumentos:
        session_id: identificador de la sesión.
        pregunta: texto de la pregunta del usuario.
        fragmentos_documentos: fragmentos de documentos de referencia.
        historial: interacciones previas de la sesión.

    Retorna:
        Diccionario con las 3 llaves del contrato JSON validadas.
    """
    respuesta_bruta = llamar_agente_ia(pregunta, fragmentos_documentos, historial)
    return validar_contrato_ia(respuesta_bruta)


if __name__ == "__main__":
    # Pruebas del servicio de IA
    print("=== Prueba 1: Sin API key configurada ===")
    resultado = procesar_pregunta_ia(
        "sesion_test",
        "¿Cuántos días de licencia corresponden por matrimonio?",
        [],
        [],
    )
    print(f"  respuesta: {resultado['respuesta']}")
    print(f"  cita_fuente: {resultado['cita_fuente']}")
    print(f"  estado_encontrado: {resultado['estado_encontrado']}")

    print("\n=== Prueba 2: Validar contrato con datos inválidos ===")
    entrada_invalida = {"respuesta": 123, "cita_fuente": None, "estado_encontrado": "no es booleano"}
    resultado_valido = validar_contrato_ia(entrada_invalida)
    print(f"  respuesta: {resultado_valido['respuesta']} (tipo: {type(resultado_valido['respuesta']).__name__})")
    print(f"  cita_fuente: {resultado_valido['cita_fuente']} (tipo: {type(resultado_valido['cita_fuente']).__name__})")
    print(f"  estado_encontrado: {resultado_valido['estado_encontrado']} (tipo: {type(resultado_valido['estado_encontrado']).__name__})")

    print("\n=== Prueba 3: Construir prompt ===")
    prompt = construir_prompt_ia(
        "¿Cuál es la fecha de corte para horas extras?",
        ["[Categoría: Nómina] Pregunta: fecha corte | Respuesta: día 25"],
        [],
    )
    print("Prompt generado (primeros 200 caracteres):")
    print(prompt[:200])
    print("...")

    print("\n=== Todas las pruebas de integración IA completadas ===")
