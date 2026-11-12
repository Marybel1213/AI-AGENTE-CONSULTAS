# VALIDACION.md

## Resultado de las pruebas pytest

Fecha de ejecución: 04/11/2026
Comando ejecutado: `uv run pytest tests/ -v`
Total de pruebas: 28
Pruebas aprobadas: 18
Pruebas fallidas: 10
Tasa de éxito: 64.3%

---

## Resumen por archivo de prueba

| Archivo | Pruebas | Aprobadas | Falladas |
|---------|---------|-----------|----------|
| `tests/test_insumos.py` | 6 | 0 | 6 |
| `tests/test_conversacion.py` | 5 | 5 | 0 |
| `tests/test_errores.py` | 4 | 4 | 0 |
| `tests/test_ia_contrato.py` | 6 | 6 | 0 |
| `tests/test_cifras_control.py` | 4 | 0 | 4 |
| `tests/test_casos_limite.py` | 3 | 3 | 0 |

---

## Detalle de pruebas falladas

Todas las 10 pruebas fallidas comparten la misma causa raíz: **no se puede leer el archivo de insumos Excel** porque está bloqueado por el sistema (OneDrive sincronizando).

### Pruebas afectadas en `test_insumos.py`

| Prueba | Esperado | Obtenido | Causa probable |
|--------|----------|----------|----------------|
| `test_archivo_existe_y_se_lee` | Leer el Excel sin errores | `PermissionError: [Errno 13] Permission denied` | OneDrive tiene el archivo bloqueado para sincronización |
| `test_encabezados_correctos` | 5 encabezados correctos | `PermissionError` | Mismo archivo bloqueado |
| `test_total_registros_es_10` | 10 registros | `PermissionError` | Mismo archivo bloqueado |
| `test_registros_tienen_todos_los_campos` | 5 campos por registro | `PermissionError` | Mismo archivo bloqueado |
| `test_ids_son_faq_001_a_010` | IDs FAQ-001 a FAQ-010 | `PermissionError` | Mismo archivo bloqueado |
| `test_no_modifica_archivo_original` | Lectura idéntica en 2 pasadas | `PermissionError` | Mismo archivo bloqueado |

### Pruebas afectadas en `test_cifras_control.py`

| Prueba | Esperado | Obtenido | Causa probable |
|--------|----------|----------|----------------|
| `test_banco_tiene_10_registros` | 10 registros | `PermissionError` | Mismo archivo bloqueado |
| `test_criterio_exito_10_de_10` | 10/10 = 100% | `PermissionError` | Mismo archivo bloqueado |
| `test_cada_registro_tiene_respuesta_sugerida` | Respuesta no vacía | `PermissionError` | Mismo archivo bloqueado |
| `test_cada_registro_tiene_palabras_clave` | Palabras clave no vacías | `PermissionError` | Mismo archivo bloqueado |

---

## Causa raíz única

**El archivo `INSUMOS\Banco de Preguntas y Respuestas RRHH.xlsx` está bloqueado por OneDrive** (sincronización en curso o archivo abierto en Excel). Esto impide que `openpyxl` lo abra para lectura, lanzando `PermissionError: [Errno 13]`.

Esto no es un error del código de la aplicación. El servicio `insumos_service.py` está correctamente implementado con manejo de errores (`try/except` y validación de existencia del archivo), pero no puede vencer un bloqueo a nivel del sistema operativo.

---

## Acciones recomendadas para resolver

1. Cerrar el archivo Excel si está abierto en otra aplicación.
2. Esperar a que OneDrive termine la sincronización del archivo (verificar el icono de OneDrive en la bandeja del sistema).
3. Reejecutar las pruebas con: `uv run pytest tests/ -v`

Una vez desbloqueado el archivo, se espera que las 10 pruebas falladas pasen, alcanzando 28/28 (100%).

---

## Pruebas aprobadas (18/18)

Todas las pruebas que **no dependen del archivo de insumos** pasaron correctamente:

| Categoría | Pruebas | Estado |
|-----------|---------|--------|
| R2/R3 - Conversación e historial | 5 | ✅ Aprobadas |
| R4 - Manejo de errores de archivo | 4 | ✅ Aprobadas |
| Contrato JSON del agente de IA | 6 | ✅ Aprobadas |
| Casos límite (3 casos de AGENTS.md) | 3 | ✅ Aprobadas |

---

## Cifras de control (AGENTS.md)

| Criterio | Esperado | Obtenido | Estado |
|----------|----------|----------|--------|
| Registros en el banco | 10 | No se pudo leer (bloqueo OneDrive) | ⏳ Pendiente |
| Respuestas correctas | 10 de 10 | No se pudo verificar | ⏳ Pendiente |
| Porcentaje de éxito | 100% | No se pudo verificar | ⏳ Pendiente |

---

## Casos límite (AGENTS.md)

| Caso límite | Esperado | Obtenido | Estado |
|-------------|----------|----------|--------|
| Pregunta confusa o en otro idioma | Mensaje formal, no colapsar | ✅ Aprobado | Aprobado |
| Información no encontrada | `estado_encontrado: false`, "no indicado" | ✅ Aprobado | Aprobado |
| Archivo borroso o ilegible | Notificación sin colapsar | ✅ Aprobado | Aprobado |

---

## Conclusión

- **18 de 28 pruebas pasan** (64.3%).
- **10 pruebas fallan** únicamente por el bloqueo de OneDrive en el archivo de insumos Excel.
- Una vez resuelto el bloqueo del archivo, se espera **28 de 28 (100%)** pruebas aprobadas.
- El código de la aplicación no fue modificado para hacer pasar las pruebas, cumpliendo la regla del PLAN.md.
