import ollama
from moderation import mensaje_permitido
from Structured_Outputs_JSON import generar_json_valido

System_Prompt = "Eres un asistente de atencion al cliente cordial y empatico."
memoria = [{"role": "system", "content": System_Prompt}]
ultimo_mensaje = None

while True:
    entrada = input("Tu: ").strip()
    
    if entrada.lower() == "salir":
        break
    
    if entrada == "/json":
        if ultimo_mensaje is None:
            print("Todavía no hay ningún mensaje para resumir.\n")
        else:
            ticket, intento = generar_json_valido(ultimo_mensaje)
            if ticket:
                print(f"\nJSON válido en {intento} intento(s):")
                print(ticket.model_dump_json(indent=2))
            else:
                print(f"No se pudo generar un JSON válido tras {intento} intentos.")
        continue  
    if entrada == "/memoria":
        for msg in memoria:
            print(f"[{msg['role']}]: {msg['content']}\n")
        continue
    
    permitido, categoria = mensaje_permitido(entrada)
    
    if not permitido:
        print(f" Error, mensaje no permitido (categoría: {categoria}).\n")
        continue
    
    memoria.append({"role": "user", "content": entrada})
    ultimo_mensaje = entrada
    
    stream = ollama.chat(
        model= "llama3.2:3b",
        messages=memoria,
        stream=True,
        options={"num_predict": 200},
    )
    print("Asistente: ", end="", flush=True)
    respuesta_completa = ""
    input_tokens= 0
    output_tokens= 0
    
    for chunk in stream:
        texto = chunk["message"]["content"]
        print(texto, end="", flush=True)
        respuesta_completa += texto
        
        if chunk.get("done"):
            input_tokens = chunk.get("prompt_eval_count", 0)
            output_tokens = chunk.get("eval_count", 0)
            
    print()
    
    print(f"[Tokens] entrada: {input_tokens} | salida: {output_tokens} | total: {input_tokens + output_tokens}")
    
    memoria.append({"role": "assistant", "content": respuesta_completa})
    
    