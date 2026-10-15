# AMISR-14 Weekly Report Automation

**Portafolio AI Engineer — Proyecto 01**

Herramienta para asistir en la preparación de informes técnicos semanales del radar AMISR-14 mediante Python, `uv`, Google Docs API y la API de OpenAI.

El sistema busca convertir tareas, notas e informes técnicos en un borrador semanal claro y verificable: qué se hizo, qué resultado se obtuvo y cuál es el estado de cada actividad. La actualización del documento compartido será controlada y, al inicio, requerirá revisión humana.

> **Principio del producto:** la IA interpreta y propone; el código valida y controla; una persona revisa y aprueba antes de modificar el documento compartido.

---

## 1. Problema que queremos resolver

La información para el informe semanal puede estar repartida entre tareas, notas y reportes técnicos. Preparar el resumen manualmente consume tiempo y puede producir inconsistencias en la redacción o en el estado de las actividades.

Este proyecto busca:

- Reunir y procesar la información de entrada de forma consistente.
- Sintetizar actividades técnicas sin perder los resultados relevantes.
- Identificar el estado de cada actividad usando evidencia disponible.
- Mantener trazabilidad entre cada resumen y sus fuentes.
- Preparar un borrador para la sección AMISR-14 del informe compartido.
- Evitar cambios accidentales en las secciones de otros responsables.

El objetivo no es que un LLM decida por sí solo qué ocurrió. El sistema debe distinguir entre hechos documentados, inferencias y datos que necesitan confirmación.

## 2. Alcance inicial del MVP

La primera versión será deliberadamente pequeña y segura.

### Incluido

1. Leer documentos de entrada autorizados.
2. Extraer y normalizar tareas e informes.
3. Usar OpenAI para proponer una síntesis estructurada.
4. Validar que cada actividad tenga evidencia suficiente y un estado permitido.
5. Generar un borrador local para revisión.
6. Mostrar qué fuentes respaldan cada afirmación.
7. Preparar la integración con Google Docs de forma que solo pueda actualizarse la sección objetivo.

### No incluido al inicio

- Actualización automática sin aprobación humana.
- Modificación de todo el documento compartido.
- Afirmar que una actividad terminó si la fuente no lo demuestra.
- Enviar información técnica sensible a un proveedor de IA sin revisar antes las políticas y autorizaciones aplicables.
- Ejecutar tareas de mantenimiento o controlar el radar.

## 3. Estados de actividad

Los estados serán controlados por el programa y no se aceptarán valores arbitrarios.

| Estado | Cuándo usarlo |
|---|---|
| `CONCLUIDA` | La evidencia indica que la actividad terminó o que se alcanzó el objetivo. |
| `EN_PROCESO` | Hay trabajo realizado, pero quedan acciones o pruebas pendientes. |
| `PENDIENTE` | La actividad está solicitada o planificada, sin ejecución documentada. |
| `BLOQUEADA` | La fuente identifica explícitamente un impedimento. |
| `POR_VERIFICAR` | La información disponible no permite determinar el estado con confianza. |

**Regla:** si no hay evidencia suficiente, el sistema debe indicar `POR_VERIFICAR` y pedir revisión; nunca debe inventar un resultado.

## 4. Tecnologías y por qué las elegimos

- **Python:** lenguaje principal para la lógica de negocio, integración y pruebas.
- **`uv`:** administración del proyecto, dependencias, entorno virtual y archivo de bloqueo.
- **OpenAI API:** síntesis de texto técnico y generación de resultados estructurados.
- **Google Drive API / Google Docs API:** localización y lectura de documentos, y más adelante actualización controlada del informe.
- **Pydantic:** validación de los datos estructurados que devuelve el modelo.
- **pytest:** pruebas automatizadas.
- **Git:** historial de cambios y colaboración.

La IA no reemplaza la lógica del sistema. Fechas, permisos, estados válidos, validaciones, selección de la sección y control de duplicados deben resolverse con código determinista siempre que sea posible.

---

## 5. Estructura del proyecto

```text
ai-engineer-01-amisr14/
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── .env.example
├── config/
│   └── settings.example.yaml
├── docs/
│   ├── architecture.md
│   ├── product-requirements.md
│   ├── google-api-setup.md
│   └── decisions/
│       └── 0001-uv-and-project-structure.md
├── samples/
│   ├── input/
│   │   └── .gitkeep
│   └── expected/
│       └── .gitkeep
├── src/
│   └── amisr_report/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── domain/
│       │   ├── __init__.py
│       │   └── models.py
│       ├── integrations/
│       │   ├── __init__.py
│       │   ├── openai_client.py
│       │   ├── google_drive.py
│       │   └── google_docs.py
│       ├── extraction/
│       │   ├── __init__.py
│       │   └── task_reader.py
│       ├── processing/
│       │   ├── __init__.py
│       │   ├── task_filter.py
│       │   └── task_normalizer.py
│       ├── analysis/
│       │   ├── __init__.py
│       │   └── report_analyzer.py
│       ├── generation/
│       │   ├── __init__.py
│       │   ├── prompts.py
│       │   └── report_generator.py
│       ├── validation/
│       │   ├── __init__.py
│       │   └── report_validator.py
│       └── output/
│           ├── __init__.py
│           ├── draft_writer.py
│           └── report_updater.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── logs/
    └── .gitkeep
```

### Responsabilidad de cada parte

| Módulo | Responsabilidad |
|---|---|
| `domain/models.py` | Define los objetos y campos que usa el producto, como actividad, resultado, estado y evidencia. |
| `integrations/openai_client.py` | Encapsula las llamadas a OpenAI; evita repartir llamadas a la API por todo el código. |
| `integrations/google_drive.py` | Busca y accede a los archivos de entrada autorizados. |
| `integrations/google_docs.py` | Lee documentos y abstrae las operaciones de Google Docs. |
| `extraction/task_reader.py` | Convierte el contenido de entrada en registros que el programa pueda procesar. |
| `processing/` | Filtra y normaliza tareas, fechas y texto sin cambiar su significado. |
| `analysis/report_analyzer.py` | Coordina el análisis asistido por IA y produce una propuesta estructurada. |
| `generation/` | Contiene las instrucciones del modelo y compone el borrador semanal. |
| `validation/report_validator.py` | Verifica campos, estados, evidencia y reglas del producto. |
| `output/draft_writer.py` | Guarda un borrador local que se puede revisar antes de publicarlo. |
| `output/report_updater.py` | En una fase posterior, actualiza únicamente el rango autorizado del documento. |
| `tests/` | Comprueba el comportamiento esperado y protege contra regresiones. |

No crearemos todos estos archivos con lógica desde el primer día. La estructura es el mapa del producto; implementaremos cada módulo cuando el flujo lo necesite. Así evitamos complejidad prematura.

---

## 6. Primeros pasos con `uv`

### 6.1. Instalar `uv`

Consulta las instrucciones oficiales para tu sistema operativo: <https://docs.astral.sh/uv/getting-started/installation/>.

Verifica la instalación:

```bash
uv --version
```

### 6.2. Crear el proyecto

Desde la carpeta donde guardarás tus proyectos:

```bash
uv init --package ai-engineer-01-amisr14
cd ai-engineer-01-amisr14
```

`--package` crea un proyecto instalable con una estructura adecuada para código dentro de `src/`. Esto facilita importar el paquete desde distintos módulos y ejecutar pruebas sin depender de rutas improvisadas.

> Si ya creaste el repositorio con archivos, no vuelvas a ejecutar `uv init` encima sin revisar primero qué generó. Conserva el `pyproject.toml` y adapta la estructura con cuidado.

### 6.3. Agregar dependencias

```bash
uv add openai pydantic python-dotenv pyyaml
uv add --dev pytest ruff
```

- `openai`: cliente oficial para la API.
- `pydantic`: valida la estructura y los tipos de los datos.
- `python-dotenv`: permite cargar variables de entorno desde un archivo local.
- `pyyaml`: lee configuración en YAML.
- `pytest`: ejecuta pruebas.
- `ruff`: revisa estilo y errores comunes de Python.

Las librerías de Google se añadirán cuando implementemos la integración y hayamos definido el mecanismo de autenticación adecuado.

### 6.4. Ejecutar Python y las pruebas

```bash
uv run python --version
uv run pytest
```

`uv run` ejecuta el comando dentro del entorno del proyecto y ayuda a mantener las dependencias alineadas con `pyproject.toml` y `uv.lock`.

### 6.5. Mantener reproducible el entorno

- Versiona `pyproject.toml` y `uv.lock`.
- No versiona el entorno virtual `.venv/`.
- Cuando otra persona clone el proyecto, puede ejecutar `uv sync` para instalar las dependencias fijadas en el lockfile.

---

## 7. Configurar la API de OpenAI con seguridad

### 7.1. Crear la variable de entorno

Crea un archivo local llamado `.env` a partir de `.env.example`. El archivo `.env` debe estar excluido de Git.

Ejemplo de `.env.example`:

```dotenv
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
```

`OPENAI_MODEL` es configurable: antes de desplegar el proyecto, confirma en la documentación de OpenAI qué modelo está disponible para tu cuenta y qué capacidades necesitas.

**Nunca escribas la clave real en el código, en el README, en capturas de pantalla ni en GitHub.** Si una clave se publica por accidente, revócala y crea otra.

### 7.2. Primera llamada de prueba

Cuando hayas configurado tu clave en `.env`, puedes crear temporalmente un archivo de prueba:

```python
# test_openai.py
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")

if not api_key:
    raise RuntimeError("Falta configurar OPENAI_API_KEY en el archivo .env")

if not model:
    raise RuntimeError("Falta configurar OPENAI_MODEL en el archivo .env")

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model=model,
    input="Responde en español con una sola frase: ¿qué es un informe técnico?"
)

print(response.output_text)
```

Ejecuta:

```bash
uv run python test_openai.py
```

Esta prueba confirma la conexión básica; todavía no es el generador de informes. Más adelante moveremos el código reutilizable a `integrations/openai_client.py` y añadiremos manejo de errores, límites de uso y validación estructurada.

Ten presente que las llamadas a la API pueden generar costos según el modelo y el uso. Configura límites y monitorea el consumo en tu cuenta.

---

## 8. Variables y configuración

El `.env.example` documenta las variables necesarias sin incluir secretos reales. La configuración funcional del producto irá en `config/settings.example.yaml`, por ejemplo:

```yaml
report:
  timezone: "America/Lima"
  status_values:
    - CONCLUIDA
    - EN_PROCESO
    - PENDIENTE
    - BLOQUEADA
    - POR_VERIFICAR

safety:
  require_human_approval: true
  allow_shared_document_write: false
```

Los identificadores de documentos y los permisos se configurarán cuando implementemos la integración con Google. Evitaremos incluir identificadores privados o credenciales en archivos públicos del repositorio.

---

## 9. Flujo de funcionamiento previsto

```text
Documentos de entrada
        |
        v
Lectura y extracción
        |
        v
Normalización de tareas
        |
        v
Análisis con OpenAI
        |
        v
Validación con reglas de negocio
        |
        v
Borrador local + evidencia de origen
        |
        v
Revisión y aprobación humana
        |
        v
Actualización controlada de la sección AMISR-14
```

La actualización de Google Docs permanecerá deshabilitada hasta que probemos el rango objetivo, los permisos y el comportamiento ante ediciones simultáneas. Si el documento cambia inesperadamente, el proceso deberá detenerse y solicitar revisión, en lugar de arriesgarse a sobrescribir contenido ajeno.

## 10. Calidad, seguridad y pruebas

Antes de considerar lista una versión, comprobaremos que:

- El estado de una actividad no se deduce sin evidencia.
- Los resúmenes no introducen resultados que no aparecen en las fuentes.
- Cada actividad puede rastrearse hasta su fuente.
- Los campos obligatorios y los estados pertenecen al esquema esperado.
- Las tareas duplicadas se detectan o se gestionan con reglas explícitas.
- Un error de API no provoca una actualización parcial del documento.
- El sistema no modifica secciones de otros responsables.
- Los cambios simultáneos en el documento se detectan antes de escribir.
- Las pruebas no requieren credenciales reales ni envían datos operativos sensibles.
- Los registros de ejecución no exponen claves ni contenido confidencial innecesario.

Para el desarrollo usaremos datos ficticios o anonimizados en `samples/` y `tests/`. Antes de enviar documentos reales a una API externa, confirmaremos que su uso esté autorizado.

## 11. Plan de desarrollo por etapas

1. **Definición del producto:** usuarios, problema, entradas, salida esperada y criterios de aceptación.
2. **Base del proyecto:** Git, `uv`, estructura `src/`, dependencias y primeras pruebas.
3. **Prueba de OpenAI:** llamada mínima, configuración segura y manejo de errores.
4. **Lectura de fuentes:** extracción de documentos de entrada en modo de solo lectura.
5. **Modelo de datos:** esquema validado para actividad, acciones, resultado, estado y evidencia.
6. **Síntesis asistida por IA:** instrucciones, ejemplos y evaluación de calidad.
7. **Borrador verificable:** generar la salida local y revisarla antes de publicar.
8. **Integración Google Docs:** autenticación, localización del rango autorizado y controles de concurrencia.
9. **Pruebas de extremo a extremo:** casos normales, datos incompletos, fallos y duplicados.
10. **Uso semanal:** ejecución supervisada, registro de resultados y mejora continua.

## 12. Criterios de éxito del MVP

El MVP estará listo para una prueba supervisada cuando:

- Genere un borrador con el formato acordado.
- Cada afirmación importante tenga una fuente identificable.
- Los estados inciertos se marquen para verificar.
- Las validaciones automáticas pasen las pruebas.
- Una persona pueda revisar y aprobar el borrador.
- La escritura en el documento compartido esté limitada a la sección autorizada y desactivada por defecto.

No mediremos el éxito solo por cuánto texto produce la IA. También importan la exactitud, el tiempo ahorrado, la facilidad de revisión y el riesgo de errores.

## 13. Buenas prácticas de Git

Ejemplo de `.gitignore`:

```gitignore
# Entorno y secretos
.venv/
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
dist/
build/
*.egg-info/

# Archivos locales y registros
logs/*
!logs/.gitkeep
samples/input/*
!samples/input/.gitkeep
```

Antes de cada commit:

```bash
uv run ruff check .
uv run pytest
git status
```

Haz commits pequeños con mensajes que expliquen el cambio, por ejemplo:

```text
chore: initialize project with uv
test: add initial report model tests
feat: add validated activity schema
```

No incluyas documentos reales del informe, credenciales, claves API ni datos operativos privados en el repositorio.

---

## 14. Nuestra forma de aprender y desarrollar

En cada etapa seguiremos este método:

1. **Entender el problema:** qué necesidad del usuario resolvemos.
2. **Diseñar la solución:** qué módulo debe asumir la responsabilidad y por qué.
3. **Implementar lo mínimo:** una mejora pequeña y verificable.
4. **Probar:** comprobar tanto el caso esperado como los errores.
5. **Reflexionar:** qué decisión tomamos, qué alternativa descartamos y qué aprendimos.
6. **Registrar:** actualizar documentación y Git.

La meta es aprender a construir software mantenible y útil, no acumular librerías ni escribir código complejo sin necesidad.

## Recursos oficiales

- [`uv` — documentación](https://docs.astral.sh/uv/)
- [OpenAI API — documentación](https://platform.openai.com/docs/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Google Docs API](https://developers.google.com/workspace/docs/api)
- [Google Drive API](https://developers.google.com/workspace/drive/api)
- [pytest](https://docs.pytest.org/)
- [Ruff](https://docs.astral.sh/ruff/)

---

**Estado actual:** diseño inicial del producto. La escritura en Google Docs todavía no está habilitada.

**Siguiente paso recomendado:** crear el repositorio, inicializarlo con `uv`, inspeccionar los archivos generados y entender `pyproject.toml` antes de implementar la primera funcionalidad.