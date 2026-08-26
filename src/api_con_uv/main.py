import os 
from dotenv import load_dotenv 
from moderation import mensaje_permitido
import ollama

def responder(mensaje_usuario, categoria):
    respuesta = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {"role": "system", "content": "Eres un asistente de atención al cliente cordial y empático. Discúlpate por la espera y ofrece una solución al cliente.Dale la respuesta en 3 frases"},
        {"role": "user", "content": mensaje_usuario}
    ],
    options={"num_predict": 100, "temperature": 0} # se definen el maximo de tokens y la temperatura del modelo
)
    return { # varios calculos de referencia para ver los tokens que entran, salen y el total.
        "content": respuesta["message"]["content"],
        "input_tokens": respuesta.get("prompt_eval_count", 0),
        "output_tokens": respuesta.get("eval_count", 0)
    }

def procesar_mensaje(mensaje):
    permitido, categoria = mensaje_permitido(mensaje)
    if permitido:
        respuesta = responder(mensaje, categoria)
        return respuesta
    else:
        return{
            "content": f"Error, la categoria de: {categoria} no esta permitida, por favor modifique su mensaje ",
            "input_tokens": 0,
            "output_tokens": 0
        }

if __name__ == "__main__":
    mensaje = "Buenas, llevo 2 dias esperando mi pedido y no ha llegado, supuestamente me lo enviaron hace 2 dias"
    resultado = procesar_mensaje(mensaje)  # <-- guardamos el resultado aqui
    print(resultado["content"])

    print("Input Tokens: ", resultado["input_tokens"])
    print("Output Tokens: ", resultado["output_tokens"])
    print("Total Tokens: ", resultado["input_tokens"] + resultado["output_tokens"])
    
    
    
    
    
    
    
    


    # EJEMPLO BASICO DE USO DE LA API DE OLLAMA
# respuesta = ollama.chat(
#     model="llama3.2:3b",
#     messages = [
#     {"role": "system", "content": "eres un experto en videojuegos"},
#     {"role": "user", "content": "cual es el mejor juego de supervivencia de la historia?"}
# ],)
# print(respuesta["message"]["content"])  # Muestra la respuesta del modelo


# def clasificar(mensaje):
    
#     respuesta = ollama.chat(
#     model="llama3.2:3b",
#     messages = [
#         {"role": "system", "content": "Eres un experto clasificador de mensajes, responde solo con una palabra"},
#         {"role": "user", "content": mensaje}
#     ],
#     options={ "num_predict": 30,"temperature": 0.4}
# )
#     return respuesta["message"]["content"]  # Devuelve la respuesta del modelo

# def responder(mensaje_usuario, categoria):
#     respuesta = ollama.chat(
#     model="llama3.2:3b",
#     messages = [
#         {"role": "system", "content": f"Eres un asistente de atención al cliente de {categoria}, responde de manera cordial y empática, no te olvides de disculparte por la espera y ofrecer una solución al cliente"},
#         {"role": "user", "content": mensaje_usuario}
#     ],
#     options={ "num_predict": 100,"temperature": 0}
# )

#     return respuesta["message"]["content"]  # Devuelve la respuesta del modelo

    
    # #llamda 1
    # categoria = clasificar(mensaje)
    # print(f"La categoría es: {categoria}")
    
    # #llamada 2
    # respuesta = responder(mensaje, categoria)
    # print(f"\nLa respuesta es:\n {respuesta}")
