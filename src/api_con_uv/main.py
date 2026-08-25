import os 
from dotenv import load_dotenv  
import ollama

load_dotenv()  # Carga las variables .env

# EJEMPLO BASICO DE USO DE LA API DE OLLAMA
# respuesta = ollama.chat(
#     model="llama3.2:3b",
#     messages = [
#     {"role": "system", "content": "eres un experto en videojuegos"},
#     {"role": "user", "content": "cual es el mejor juego de supervivencia de la historia?"}
# ],)
# print(respuesta["message"]["content"])  # Muestra la respuesta del modelo




def clasificar(mensaje):
    
    respuesta = ollama.chat(
    model="llama3.2:3b",
    messages = [
        {"role": "system", "content": "Eres un experto clasificador de mensajes, responde solo con una palabra"},
        {"role": "user", "content": mensaje}
    ],
    options={ "num_predict": 30,"temperature": 0.4}
)
    return respuesta["message"]["content"]  # Devuelve la respuesta del modelo

def responder(mensaje_usuario, categoria):
    respuesta = ollama.chat(
    model="llama3.2:3b",
    messages = [
        {"role": "system", "content": f"Eres un asistente de atención al cliente de {categoria}, responde de manera cordial y empática, no te olvides de disculparte por la espera y ofrecer una solución al cliente"},
        {"role": "user", "content": mensaje_usuario}
    ],
    options={ "num_predict": 100,"temperature": 0}
)

    return respuesta["message"]["content"]  # Devuelve la respuesta del modelo

if __name__ == "__main__":
    mensaje = "Buenas, llevo 2 dias esperando mi pedido y no ha llegado, supuestamente me lo enviaron hace 2 dias"
    
    #llamda 1
    categoria = clasificar(mensaje)
    print(f"La categoría es: {categoria}")
    
    #llamada 2
    respuesta = responder(mensaje, categoria)
    print(f"\nLa respuesta es:\n {respuesta}")