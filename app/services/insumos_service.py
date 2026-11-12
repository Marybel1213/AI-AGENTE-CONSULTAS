"""
Servicio de lectura de insumos.

Lee el archivo Excel de la carpeta INSUMOS y expone los datos estructurados
del banco de preguntas y respuestas de RRHH.

Regla de negocio: nunca modifica los archivos de INSUMOS.
"""

import os
import openpyxl


INSUMOS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "INSUMOS")
EXCEL_FILENAME = "Banco de Preguntas y Respuestas RRHH.xlsx"


def leer_insumos_excel():
    """
    Lee el archivo Excel de insumos y devuelve los encabezados y los registros.

    Retorna:
        dict con claves:
            - encabezados: lista de nombres de columna
            - registros: lista de diccionarios, uno por fila de datos
            - total_registros: cantidad de filas de datos
    """
    ruta_excel = os.path.join(INSUMOS_DIR, EXCEL_FILENAME)

    if not os.path.exists(ruta_excel):
        raise FileNotFoundError(f"No se encontró el archivo de insumos: {ruta_excel}")

    wb = openpyxl.load_workbook(ruta_excel, read_only=True, data_only=True)
    ws = wb.active

    filas = list(ws.iter_rows(values_only=True))
    wb.close()

    # Las filas 1-2 son título y descripción (metadatos, no datos estructurados)
    # Las filas 3-4 son metadatos del banco
    # La fila 5 son los encabezados de datos
    # Las filas 6 en adelante son los registros

    if len(filas) < 6:
        raise ValueError("El archivo de insumos no tiene suficientes filas de datos.")

    encabezados = [str(c) if c is not None else "" for c in filas[4]]

    registros = []
    for fila in filas[5:]:
        if all(celda is None for celda in fila):
            continue
        registro = {}
        for i, encabezado in enumerate(encabezados):
            valor = fila[i] if i < len(fila) else None
            registro[encabezado] = valor
        registros.append(registro)

    return {
        "encabezados": encabezados,
        "registros": registros,
        "total_registros": len(registros),
    }


if __name__ == "__main__":
    datos = leer_insumos_excel()
    print("Encabezados:", datos["encabezados"])
    print("Total registros:", datos["total_registros"])
    for reg in datos["registros"]:
        print(reg)
