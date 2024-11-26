import streamlit as st
import time
import requests


# Función para inicializar el cliente de la API de Groq
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


def main():
    # Título principal de la aplicación
    st.title("Asistente Virtual de Pedidos de Sushi 24/7")

    # Solicitar la API Key para Groq
    if "api_key" not in st.session_state:
        st.session_state["api_key"] = ""

    st.sidebar.header("Configuración del API de Groq")
    st.session_state["api_key"] = st.sidebar.text_input(
        "Introduce tu API Key de Groq:", type="password"
    )

    if not st.session_state["api_key"]:
        st.warning("Por favor, introduce tu API Key para continuar.")
        return

    # Inicialización del cliente Groq
    groq_client = GroqAPI(api_key=st.session_state["api_key"])

    # Sección de configuración del asistente virtual
    st.sidebar.header("Configuración del Asistente")
    bot_name = st.sidebar.text_input("Nombre del asistente virtual:", value="SushiBot")
    prompt_default = f"""Eres un asistente virtual llamado {bot_name}, especializado en tomar pedidos de sushi y proporcionar información sobre el menú. Respondes de forma clara y amable, y haces preguntas relevantes para completar el pedido del cliente."""
    bot_description = st.sidebar.text_area("Descripción del asistente virtual:", value=prompt_default)

    # Inicialización del historial de chat
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Entrada del usuario
    st.subheader("Interacción")
    user_input = st.text_input("Escribe tu pedido o consulta:", key="user_input")

    if st.button("Enviar"):
        if user_input.strip() == "":
            st.warning("Por favor, escribe algo antes de enviar.")
        else:
            # Agregar el mensaje del usuario al historial
            st.session_state["chat_history"].append({"role": "user", "content": user_input})

            # Preparar los mensajes para la API
            messages = st.session_state["chat_history"]

            # Generar respuesta a través de la API de Groq
            start_time = time.time()
            response_content = groq_client.chat(model="llama3-8b-8192", messages=messages)
            end_time = time.time()

            # Agregar la respuesta del bot al historial
            st.session_state["chat_history"].append({"role": "assistant", "content": response_content})

            # Mostrar respuesta
            st.markdown(f"**🍣 {bot_name}:** {response_content}")
            st.info(f"⏱️ Tiempo de respuesta: {round(end_time - start_time, 2)} segundos.")

    # Visualización del historial de chat
    st.subheader("Historial de Chat")
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(f"**🤵 Cliente:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**🍣 {bot_name}:** {msg['content']}")

    # Informacion de resumen
    st.sidebar.subheader("Estadísticas del Chat")
    total_messages = len(st.session_state["chat_history"])
    user_messages = len([msg for msg in st.session_state["chat_history"] if msg["role"] == "user"])
    assistant_messages = len([msg for msg in st.session_state["chat_history"] if msg["role"] == "assistant"])

    st.sidebar.metric("Mensajes Totales", total_messages)
    st.sidebar.metric("Mensajes de Clientes", user_messages)
    st.sidebar.metric("Respuestas del Bot", assistant_messages)

    # Mensaje de personalización
    st.sidebar.info("Puedes personalizar la descripción y el nombre del asistente para adaptarlo a tus necesidades.")


# Punto de entrada principal
if __name__ == '__main__':
    main()