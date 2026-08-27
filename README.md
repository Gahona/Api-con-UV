Markdown
# Pydantic LLM Output Validation (con Ollama)

Este proyecto es una prueba de concepto para validar respuestas estructuradas de un Modelo de Lenguaje (LLM) en entorno local mediante el uso de Pydantic y Ollama (llama3.2:3b).

---

## Objetivo

Garantizar que las salidas generadas por un modelo de lenguaje cumplan estrictamente con un contrato de datos (tipos de datos, rangos numéricos, listas de opciones estrictas y campos obligatorios/opcionales) antes de ser consumidas por una aplicación.

---

## Características Clave

* Contrato de Datos con Pydantic: Uso de BaseModel y restricciones Field() (como ge, le, min_length, max_length).
* Modelos Locales: Integración directa con el modelo local llama3.2:3b mediante la librería oficial de ollama.
* Traducción de Esquemas: Extracción dinámica del JSON Schema (model_json_schema()) para guiar las respuestas del modelo.
* Lógica de Reintentos (Retry Logic): Sistema de autocorregido que reenvía los errores de ValidationError al propio LLM para que ajuste su salida si se equivoca en el primer intento.

---

## Requisitos Previos

* Python 3.10+
* Ollama instalado localmente con el modelo llama3.2:3b servido:
  ```bash
  ollama run llama3.2:3b
Instalación
Clona la rama e instala las dependencias necesarias:

Bash
pip install pydantic ollama
(O mediante uv: uv pip install pydantic ollama)


Estructura del Modelo (Ejemplo)

from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class RespuestaAnalisis(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100)
    puntuacion: float = Field(..., ge=0.0, le=10.0)
    categoria: Literal["tecnologia", "ciencia", "general"]
    etiquetas: List[str] = Field(..., min_length=1)
    notas_adicionales: Optional[str] = Field(default=None, max_length=200)
    
## Uso
Para ejecutar las pruebas con reintentos automáticos y validación estricta:

Bash
python main.py
