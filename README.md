# Chat CLI con moderación, memoria, streaming y salida JSON validada

Proyecto de práctica en Python que combina un modelo local (vía [Ollama](https://ollama.com)) con:

- **Moderación** de mensajes antes de responder.
- **Memoria** de conversación (el modelo recuerda los turnos anteriores).
- **Streaming** de respuestas (se imprimen en vivo, token a token).
- **Structured Output** con reintentos: extracción de datos en JSON validado con `pydantic`.

## Requisitos

- Python 3.11+ (ver `.python-version`)
- [uv](https://docs.astral.sh/uv/) como gestor de entorno/dependencias
- [Ollama](https://ollama.com) corriendo localmente, con el modelo descargado:

```bash
ollama pull llama3.2:3b
```

Las dependencias del proyecto (`ollama`, `pydantic`, `python-dotenv`) están gestionadas por `uv` y se listan en `pyproject.toml`.

## Instalación

```bash
uv sync
```

## Estructura del proyecto

src/api_con_uv/
├── main.py # Script original: procesa un único mensaje (moderación + respuesta)
├── moderation.py # Clasifica si un mensaje está permitido y en qué categoría
├── Structured_Outputs_JSON.py # Genera un JSON validado (categoria, resumen, sentimiento) con reintentos
└── Cli_IA.py # CLI de chat interactivo: memoria + streaming + moderación + comando /json


## Uso

### Chat interactivo (`Cli_IA.py`)

```bash
uv run python .\src\api_con_uv\Cli_IA.py
```

Comandos disponibles dentro del chat:

| Comando   | Descripción                                                              |
|-----------|---------------------------------------------------------------------------|
| `salir`   | Termina la conversación                                                   |
| `/json`   | Genera un resumen estructurado (JSON validado) del último mensaje enviado |

Cada respuesta del asistente muestra además las métricas de tokens usados:

[Tokens] entrada: 114 | salida: 150 | total: 264


### Generar JSON estructurado por separado (`Structured_Outputs_JSON.py`)

```bash
uv run python .\src\api_con_uv\Structured_Outputs_JSON.py
```

Corre una prueba de ejemplo que:

1. Envía un mensaje al modelo pidiendo un JSON con el esquema `Comentarios` (`categoria`, `resumen`, `sentimiento`).
2. Restringe la generación al schema real usando `format=Comentarios.model_json_schema()`.
3. Valida la respuesta con `pydantic`; si falla, reintenta hasta 3 veces.

### Script original (`main.py`)

```bash
uv run python .\src\api_con_uv\main.py
```

Procesa un único mensaje: lo modera y, si está permitido, genera una respuesta de atención al cliente (limitada a 3 frases), mostrando además las métricas de tokens de esa llamada.

## Cómo funciona la moderación

`moderation.py` usa el propio modelo (`llama3.2:3b`) como clasificador:

1. `clasificar_mensaje(mensaje)` le pide al modelo, con salida JSON restringida (`pydantic` + `format`), que devuelva una única categoría: alguna de las prohibidas (`acoso`, `violencia`, `discriminación`, `pornografía`, `sexual`, `discurso de odio`, `terrorismo`, `suicidio`, `autolesiones`) o `ninguna` si el mensaje es normal.
2. `mensaje_permitido(mensaje)` devuelve `(permitido, categoria)`: `permitido` es `False` si la categoría devuelta está dentro del set `Categorias_Prohibidas`.

## Cómo funciona el JSON validado (retry-based structured output)

1. Se define un esquema con `pydantic`:

```python
class Comentarios(BaseModel):
    categoria: str
    resumen: str
    sentimiento: str
```

2. Se le pasa ese esquema a Ollama en el parámetro `format`, forzando que la generación respete esos campos exactos.
3. La respuesta se valida con `Comentarios.model_validate_json(...)`.
4. Si la validación falla, se reintenta (hasta `max_intentos`, por defecto 3), mostrando el error de cada intento en consola.

## Notas

- El límite de longitud de respuesta se controla con `options={"num_predict": ...}` en la llamada a `ollama.chat()`.
- La memoria de la conversación es en memoria (RAM): se pierde al cerrar el programa. No hay persistencia en disco todavía.

## Próximos pasos

- Persistencia de la memoria en disco (actualmente se pierde al cerrar `Cli_IA.py`).
- Revisar el schema de `Comentarios` para mensajes que no sean quejas de clientes (por ejemplo, consultas informativas).