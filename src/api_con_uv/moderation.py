import ollama
from pydantic import BaseModel

Categorias_Prhoibidas = {"acoso", "violencia", "discriminación", "pornografía", "sexual", "discurso de odio", "terrorismo", "suicidio", "autolesiones"}

class Clasificacion(BaseModel):
    categoria: str

def clasificar_mensaje(mensaje: str) -> str:
    respuesta = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": "Clasifica el mensaje en una sola categoría: acoso, violencia, discriminación, pornografía, sexual, discurso de odio, terrorismo, suicidio, autolesiones."},
            {"role": "user", "content": mensaje}
        ],
        format=Clasificacion.model_json_schema(),
        options={"num_predict": 30, "temperature": 0.2}
    )
    data = Clasificacion.model_validate_json(respuesta.message.content)
    return data.categoria.lower()

def mensaje_permitido(mensaje: str) -> tuple[bool, str]:
    categoria = clasificar_mensaje(mensaje)
    permitido = categoria not in Categorias_Prhoibidas
    return permitido, categoria

