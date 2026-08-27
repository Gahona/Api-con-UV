import json
from typing import List, Optional, Literal, Tuple
from pydantic import BaseModel, Field, ValidationError
import ollama


# =====================================================================
# 1. MODELO DE DATOS (Pydantic BaseModel)
# Define la estructura estricta y las reglas de validación del JSON.
# =====================================================================
class RespuestaAnalisis(BaseModel):
    # Campo texto obligatorio con límites de caracteres
    titulo: str = Field(..., min_length=3, max_length=100, description="Título del análisis")
    
    # Campo numérico obligatorio con rango permitido (0.0 a 10.0)
    puntuacion: float = Field(..., ge=0.0, le=10.0, description="Puntuación dada de 0 a 10")
    
    # Campo obligatorio restringido a solo 3 valores concretos
    categoria: Literal["tecnologia", "ciencia", "general"] = Field(..., description="Categoría principal")
    
    # Lista de textos que debe contener al menos 1 elemento
    etiquetas: List[str] = Field(..., min_length=1, description="Lista de palabras clave")
    
    # Campo opcional: si no viene en el JSON, su valor por defecto es None
    notas_adicionales: Optional[str] = Field(default=None, max_length=200, description="Notas extra")


# =====================================================================
# 2. FUNCIÓN DE CONSULTA CON REINTENTOS (Retry Logic)
# Llama a Ollama y, si la validación falla, le reenvía el error al LLM
# para que corrija su respuesta automáticamente en el siguiente intento.
# =====================================================================
def call_llm_with_retry(
    user_query: str, 
    max_retries: int = 3, 
    model_name: str = "llama3.2:3b"
) -> Tuple[Optional[RespuestaAnalisis], int]:
    
    # Convertimos el modelo de Pydantic a un JSON Schema legible para el LLM
    schema_json = json.dumps(RespuestaAnalisis.model_json_schema(), indent=2)

    # Creamos el historial inicial de la conversación (System + User)
    messages = [
        {
            'role': 'system',
            'content': f"""
            Eres un asistente de datos estructurados. Responde ÚNICAMENTE con un objeto JSON válido.
            No agregues introducciones, texto ni etiquetas de código Markdown.
            
            Esquema estricto que debes cumplir:
            {schema_json}
            """
        },
        {'role': 'user', 'content': user_query}
    ]

    # Bucle de reintentos
    for intento in range(1, max_retries + 1):
        print(f" Intento {intento} de {max_retries}...")

        try:
            # Petición a Ollama forzando el formato JSON
            response = ollama.chat(
                model=model_name,
                format='json',   # Fuerza sintaxis JSON válida
                messages=messages
            )
            raw_text = response['message']['content']

            # Intentamos parsear y validar el texto recibido usando Pydantic
            validated_data = RespuestaAnalisis.model_validate_json(raw_text)
            
            print(f" ¡Validación exitosa en el intento {intento}!")
            return validated_data, intento

        except ValidationError as e:
            # Extraemos los errores de Pydantic formateados (campo -> mensaje de error)
            errores = [f"- Campo '{err['loc'][0]}': {err['msg']}" for err in e.errors()]
            error_msg = "\n".join(errores)

            print(f" El intento {intento} falló la validación:")
            print(error_msg)

            # Si aún nos quedan intentos, alimentamos la conversación con el error
            if intento < max_retries:
                # 1. Guardamos la respuesta incorrecta que generó el modelo
                messages.append({'role': 'assistant', 'content': raw_text})
                
                # 2. Le enviamos al modelo el mensaje de error para que se pueda autocorregir
                messages.append({
                    'role': 'user',
                    'content': f"""
                    Tu respuesta previa falló en la validación de Pydantic por esto:
                    {error_msg}
                    
                    Por favor, corrige el JSON para cumplir con todos los tipos y restricciones.
                    """
                })

        except Exception as e:
            # Captura de errores externos (fallo de conexión con Ollama, servicio caído, etc.)
            print(f" Error inesperado de ejecución: {e}")
            break

    print(" Se superaron todos los reintentos sin conseguir un JSON válido.")
    return None, max_retries


# =====================================================================
# 3. EJECUCIÓN DE PRUEBA
# =====================================================================
if __name__ == "__main__":
    consulta = "Analiza los últimos avances en teléfonos móviles y dame tu opinión."
    
    # Ejecutamos la función de consulta con reintentos
    resultado, intentos_totales = call_llm_with_retry(consulta)

    # Imprimimos los resultados si la validación fue exitosa
    if resultado:
        print("\n---  RESULTADO FINAL VALIDADO ---")
        # model_dump_json() convierte el objeto Pydantic de vuelta a un formato JSON bonito
        print(resultado.model_dump_json(indent=2))