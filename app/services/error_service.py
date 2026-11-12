"""
Servicio de manejo de errores.

Implementa la regla de negocio R4:
    Si se detecta un error de archivo ilegible, el código debe interceptar la
    falla y mostrar la notificación correspondiente sin colapsar.

Este servicio proporciona funciones seguras para leer archivos y manejar
errores de forma controlada, devolviendo notificaciones claras en lugar de
dejar que la aplicación se cierre.
"""

from typing import Optional, Tuple


def leer_archivo_seguro(ruta_archivo: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Intenta leer un archivo de forma segura, interceptando cualquier error.

    Argumentos:
        ruta_archivo: ruta del archivo a leer.

    Retorna:
        Tupla (exito, contenido, error):
            - exito: True si se leyó correctamente, False si hubo error.
            - contenido: texto del archivo si exito es True, None si falló.
            - error: mensaje de error descriptivo si falló, None si tuvo éxito.

    Reglas aplicadas:
        - Nunca colapsa la aplicación: cualquier excepción se captura.
        - Devuelve una notificación clara y legible al usuario.
    """
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        return True, contenido, None
    except FileNotFoundError:
        return False, None, (
            "No se pudo leer el archivo de origen: el archivo no existe o "
            "fue movido o eliminado."
        )
    except PermissionError:
        return False, None, (
            "No se pudo leer el archivo de origen: no se tienen permisos "
            "para acceder al archivo."
        )
    except UnicodeDecodeError:
        return False, None, (
            "No se pudo leer el archivo de origen: el archivo está borroso, "
            "está corrupto o no tiene un formato de texto legible."
        )
    except Exception as e:  # pylint: disable=broad-except
        return False, None, (
            f"No se pudo leer el archivo de origen: error inesperado ({type(e).__name__})."
        )


def notificar_archivo_ilegrable(ruta_archivo: str) -> dict:
    """
    Genera una notificación estructurada cuando un archivo no se puede leer.

    Argumentos:
        ruta_archivo: ruta del archivo que falló.

    Retorna:
        Diccionario con claves: archivo, legible, mensaje, accion_recomendada.
    """
    exito, _, error = leer_archivo_seguro(ruta_archivo)

    if exito:
        return {
            "archivo": ruta_archivo,
            "legible": True,
            "mensaje": None,
            "accion_recomendada": None,
        }

    return {
        "archivo": ruta_archivo,
        "legible": False,
        "mensaje": error,
        "accion_recomendada": (
            "Verifique que el archivo exista, que no esté abierto en otro "
            "programa y que tenga un formato legible. Si el problema persiste, "
            "contacte al administrador del sistema."
        ),
    }


if __name__ == "__main__":
    # Pruebas de R4
    print("=== Prueba R4: Archivo existente y legible ===")
    exito, contenido, error = leer_archivo_seguro("app/__init__.py")
    print(f"  Éxito: {exito}, Contenido leído: {contenido is not None}, Error: {error}")

    print("\n=== Prueba R4: Archivo inexistente ===")
    exito, contenido, error = leer_archivo_seguro("INSUMOS/archivo_inexistente.pdf")
    print(f"  Éxito: {exito}, Contenido: {contenido}, Error: {error}")

    print("\n=== Prueba R4: Notificación estructurada ===")
    notificacion = notificar_archivo_ilegrable("INSUMOS/documento_corrupto.pdf")
    for clave, valor in notificacion.items():
        print(f"  {clave}: {valor}")

    print("\n=== Todas las pruebas de R4 completadas ===")
