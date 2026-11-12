"""
Servicio de conversación.

Implementa las reglas de negocio R2 y R3:
    R2: El código debe gestionar el flujo de la conversación y enviar la
        consulta junto con los documentos de referencia al modelo de IA.
    R3: El sistema debe registrar el historial de interacciones de la sesión
        para mantener el contexto de la conversación.

Este servicio mantiene el historial en memoria (por sesión) y prepara el
contexto (pregunta + fragmentos de documentos de referencia) para ser enviado
al agente de IA en la entrega 6.

Regla de negocio: nunca inventa información. Si no hay documentos de referencia,
el contexto se construye solo con la pregunta del usuario.
"""

from typing import Dict, List, Optional
from app.services.insumos_service import leer_insumos_excel

# Historial de conversaciones en memoria: { session_id: [ {pregunta, respuesta, cita_fuente, estado_encontrado}, ... ] }
_historial_sesiones: Dict[str, List[dict]] = {}
_error_lectura: Optional[str] = None


def obtener_historial(session_id: str) -> List[dict]:
    """
    Devuelve el historial de interacciones de una sesión.

    Argumentos:
        session_id: identificador de la sesión de conversación.

    Retorna:
        Lista de diccionarios con las interacciones previas de la sesión.
    """
    return _historial_sesiones.get(session_id, [])


def registrar_interaccion(
    session_id: str,
    pregunta: str,
    respuesta: str,
    cita_fuente: str,
    estado_encontrado: bool,
) -> None:
    """
    Registra una interacción en el historial de la sesión.

    Argumentos:
        session_id: identificador de la sesión.
        pregunta: texto de la pregunta del usuario.
        respuesta: respuesta generada por el agente de IA.
        cita_fuente: documento de donde se obtuvo la respuesta.
        estado_encontrado: True si la respuesta está en los documentos.
    """
    if session_id not in _historial_sesiones:
        _historial_sesiones[session_id] = []

    _historial_sesiones[session_id].append(
        {
            "pregunta": pregunta,
            "respuesta": respuesta,
            "cita_fuente": cita_fuente,
            "estado_encontrado": estado_encontrado,
        }
    )


def limpiar_historial(session_id: str) -> None:
    """
    Elimina el historial de una sesión (botón "Nueva conversación").
    """
    _historial_sesiones.pop(session_id, None)


def obtener_fragmentos_documentos() -> List[str]:
    """
    Extrae fragmentos de documentos de referencia desde el insumo de Excel.

    Regla: solo se leen los datos existentes, nunca se inventan fragmentos.

    Retorna:
        Lista de strings con fragmentos relevantes de los documentos de insumos.
    """
    fragmentos: List[str] = []

    try:
        datos = leer_insumos_excel()
        for registro in datos["registros"]:
            pregunta = registro.get("Pregunta Frecuente", "")
            respuesta = registro.get("Respuesta Sugerida/Ficticia", "")
            categoria = registro.get("Categoría", "")
            if pregunta and respuesta:
                fragmentos.append(
                    f"[Categoría: {categoria}] Pregunta: {pregunta} | Respuesta: {respuesta}"
                )
    except Exception as e:
        global _error_lectura
        _error_lectura = str(e)

    return fragmentos


def obtener_error_lectura() -> Optional[str]:
    """
    Devuelve el error de lectura del insumo, si lo hubo.

    Retorna:
        Mensaje de error o None si no hubo error.
    """
    return _error_lectura


def preparar_contexto_ia(session_id: str, pregunta: str) -> dict:
    """
    Prepara el contexto que se enviará al agente de IA.

    Incluye:
        - La pregunta del usuario
        - Los fragmentos de documentos de referencia disponibles
        - El historial de la sesión para mantener contexto

    Argumentos:
        session_id: identificador de la sesión.
        pregunta: texto de la pregunta actual.

    Retorna:
        Diccionario con las claves: pregunta, fragmentos_documentos, historial_sesion.
    """
    return {
        "pregunta": pregunta,
        "fragmentos_documentos": obtener_fragmentos_documentos(),
        "historial_sesion": obtener_historial(session_id),
    }


if __name__ == "__main__":
    # Prueba rápida del servicio
    session_id = "sesion_prueba_001"

    print("=== Prueba R3: Registro de historial ===")
    registrar_interaccion(
        session_id,
        "¿Cuál es la fecha de corte para horas extras?",
        "El corte es el día 25 de cada mes a las 6:00 p.m.",
        "Banco de Preguntas y Respuestas RRHH.xlsx",
        True,
    )
    registrar_interaccion(
        session_id,
        "¿Dónde consulto el recibo de pago?",
        "Desde el Portal del Colaborador o app móvil corporativa.",
        "Banco de Preguntas y Respuestas RRHH.xlsx",
        True,
    )

    historial = obtener_historial(session_id)
    print(f"Historial de la sesión '{session_id}':")
    for i, interaccion in enumerate(historial, 1):
        print(f"  {i}. Pregunta: {interaccion['pregunta']}")
        print(f"     Respuesta: {interaccion['respuesta']}")
        print(f"     Fuente: {interaccion['cita_fuente']}")
        print(f"     Encontrado: {interaccion['estado_encontrado']}")
        print()

    print("=== Prueba R2: Preparar contexto para IA ===")
    contexto = preparar_contexto_ia(session_id, "¿Cuántos días de vacaciones corresponden?")
    print("Pregunta:", contexto["pregunta"])
    print("Fragmentos de documentos:", len(contexto["fragmentos_documentos"]), "encontrados")
    print("Historial en contexto:", len(contexto["historial_sesion"]), "interacciones previas")

    print("\n=== Prueba R3: Limpiar historial (Nueva conversación) ===")
    limpiar_historial(session_id)
    historial_despues = obtener_historial(session_id)
    print(f"Historial después de limpiar: {len(historial_despues)} interacciones")

    print("\n=== Todas las pruebas de R2 y R3 completadas ===")
