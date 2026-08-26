import ollama 
from pydantic import BaseModel, ValidationError

class Comentarios(BaseModel):
    categoria: str
    resumen: str
    sentimiento: str
    
def generar_json_valido(mensaje, max_intentos=3):
    prompt = f"Analiza este mensaje y responde solo con JSON: {mensaje}"
    for intento in range(1, max_intentos +1):
        respuesta = ollama.chat(
                model="llama3.2:3b",
                messages=[{"role": "user", "content": prompt}],
                format=Comentarios.model_json_schema(),
            )
        String_con_Json = respuesta["message"]["content"]   # string que pilla el formato de json 
    
        try:
            ticket = Comentarios.model_validate_json(String_con_Json)
            return ticket, intento
        except ValidationError as e:
            print(f"[Intento {intento}] Falló la validación: {e}")
    return None, max_intentos

if __name__ == "__main__":
    mensaje = "Buenas, llevo 2 días esperando mi pedido y todavía no ha llegado. Se supone que lo enviaron hace 2 días."

    ticket, intento = generar_json_valido(mensaje)

    if ticket:
        print(f"Json valido en {intento} intentos:")
        print(ticket.model_dump_json(indent=2))
    else:
        print(f"No se pudo validar el Json tras {intento} intentos.")