# -*- coding: utf-8 -*-
"""taller_principiante.ipynb

Importar las bibliotecas necesarias
Esta celda importa las bibliotecas requeridas, como time y requests, para manejar el tiempo y las solicitudes HTTP.
"""

# Importar las bibliotecas necesarias
import time
import requests

"""Clase para manejar la API de Groq
Esta celda define una clase para interactuar con la API de Groq.
"""

# Clase para inicializar el cliente de la API de Groq
class GroqAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def chat(self, model, messages):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Lo siento, no puedo procesar tu solicitud en este momento.")
        else:
            return f"Error: {response.status_code} - {response.text}"

"""Funciones auxiliares
Esta celda contiene funciones auxiliares para estructurar el programa.
"""

def obtener_api_key():
    """Solicita y valida la API Key del usuario."""
    api_key = input("Por favor, introduce tu API Key de Groq: ").strip()
    if not api_key:
        print("Error: La API Key es obligatoria para continuar.")
        return None
    return api_key

def configurar_asistente():
    """Configura el nombre y el prompt inicial del asistente."""
    bot_name = input("Escribe el nombre del asistente virtual (por defecto es 'SushiBot'): ").strip() or "SushiBot"
    prompt_default = f"""Eres un asistente virtual llamado {bot_name}, especializado en tomar pedidos de sushi y proporcionar información sobre el menú. Respondes de forma clara y amable, y haces preguntas relevantes para completar el pedido del cliente."""
    print(f"Asistente '{bot_name}' configurado correctamente.")
    chat_history = [{"role": "system", "content": prompt_default}]
    return bot_name, chat_history

def solicitar_mensaje_usuario():
    """Solicita el mensaje del usuario."""
    user_input = input("\nCliente: ").strip()
    return user_input

def generar_respuesta(groq_client, chat_history):
    """Genera la respuesta del asistente utilizando la API de Groq."""
    start_time = time.time()
    response_content = groq_client.chat(model="llama3-8b-8192", messages=chat_history)
    end_time = time.time()
    response_time = round(end_time - start_time, 2)
    return response_content, response_time

def mostrar_respuesta(bot_name, response_content, response_time):
    """Muestra la respuesta del asistente y el tiempo de respuesta."""
    print(f"\n{bot_name}: {response_content}")
    print(f"Tiempo de respuesta: {response_time} segundos.")

def mostrar_historial(chat_history, bot_name):
    """Imprime el historial completo de la conversación."""
    print("\nHistorial de la conversación:")
    for msg in chat_history:
        role = "Cliente" if msg["role"] == "user" else ("Sistema" if msg["role"] == "system" else bot_name)
        print(f"{role}: {msg['content']}")

"""Función principal
Esta celda contiene la lógica principal del asistente virtual.
"""

def main():
    """Función principal del programa."""
    print("Bienvenido al Asistente Virtual de Pedidos de Sushi 24/7")

    # Solicitar la API Key de Groq
    api_key = obtener_api_key()
    if not api_key:
        return

    groq_client = GroqAPI(api_key)

    # Configuración del asistente
    bot_name, chat_history = configurar_asistente()

    # Solicitar mensaje del usuario
    user_input = solicitar_mensaje_usuario()
    if not user_input.lower() in ["salir", "exit"]:
        # Agregar mensaje del cliente al historial
        chat_history.append({"role": "user", "content": user_input})

        # Generar respuesta del bot
        response_content, response_time = generar_respuesta(groq_client, chat_history)

        # Agregar respuesta del bot al historial
        chat_history.append({"role": "assistant", "content": response_content})

        # Mostrar respuesta
        mostrar_respuesta(bot_name, response_content, response_time)
    else:
        print("Gracias por usar el asistente. ¡Hasta luego!")
        return

    # Continuar la conversación sin ciclo while
    while True:
        user_input = input("\n¿Deseas agregar algo más a tu pedido o tienes más preguntas? (Escribe 'no' para finalizar): ").strip()
        if user_input.lower() in ["no", "salir", "exit"]:
            print("Gracias por usar el asistente. ¡Hasta luego!")
            break
        else:
            # Agregar mensaje del cliente al historial
            chat_history.append({"role": "user", "content": user_input})

            # Generar respuesta del bot
            response_content, response_time = generar_respuesta(groq_client, chat_history)

            # Agregar respuesta del bot al historial
            chat_history.append({"role": "assistant", "content": response_content})

            # Mostrar respuesta
            mostrar_respuesta(bot_name, response_content, response_time)

    # Mostrar historial al final
    mostrar = input("¿Deseas ver el historial completo de la conversación? (s/n): ").strip().lower()
    if mostrar == "s":
        mostrar_historial(chat_history, bot_name)

"""Ejecutar el programa
Esta celda ejecuta la función principal.
"""

# Ejecutar el programa
if __name__ == "__main__":
    main()
