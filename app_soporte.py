import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Configuración inicial del modelo de lenguaje
llm = Ollama(model="llama3.1:latest")


def main():
    # Título principal de la aplicación
    st.title("Chat con Llama 3.1 para Soporte 24/7")

    # Sección de configuración del asistente virtual
    st.sidebar.header("Configuración del Asistente")
    bot_name = st.sidebar.text_input("Nombre del asistente virtual:", value="Bot")
    prompt_default = f"""Eres un asistente virtual llamado {bot_name}, especializado en soporte técnico de nivel 1. Respondes de forma simple y clara, y realizas preguntas relevantes para recopilar más detalles del problema del usuario. También haces preguntas básicas para conocer al usuario."""
    bot_description = st.sidebar.text_area("Descripción del asistente virtual:", value=prompt_default)

    # Inicialización del historial de chat
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Plantilla de prompt para el asistente
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", bot_description),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    chain = prompt_template | llm

    # Entrada del usuario
    st.subheader("Interacción")
    user_input = st.text_input("Escribe tu pregunta o consulta:", key="user_input")

    # Botón de envío
    if st.button("Enviar"):
        if user_input.lower() == "adios":
            st.write("👋 ¡Gracias por usar el asistente! Hasta luego.")
            st.stop()
        else:
            # Generación de respuesta del asistente
            response = chain.invoke({
                "input": user_input,
                "chat_history": st.session_state["chat_history"]
            })
            st.session_state["chat_history"].append(HumanMessage(content=user_input))
            st.session_state["chat_history"].append(AIMessage(content=response))

    # Visualización del historial de chat
    st.subheader("Historial de Chat")
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):
            st.markdown(f"**🤵 Humano:** {msg.content}")
        elif isinstance(msg, AIMessage):
            st.markdown(f"**📠 {bot_name}:** {msg.content}")

    # Gráficos para analizar el uso del chat
    st.sidebar.subheader("Estadísticas del Chat")
    total_messages = len(st.session_state["chat_history"])
    human_messages = len([msg for msg in st.session_state["chat_history"] if isinstance(msg, HumanMessage)])
    ai_messages = len([msg for msg in st.session_state["chat_history"] if isinstance(msg, AIMessage)])

    st.sidebar.metric("Mensajes Totales", total_messages)
    st.sidebar.metric("Mensajes Humanos", human_messages)
    st.sidebar.metric("Respuestas del Bot", ai_messages)

    # Gráfico de proporción de mensajes
    if total_messages > 0:
        st.sidebar.subheader("Distribución de Mensajes")
        st.sidebar.bar_chart({
            "Tipo de Mensaje": ["Humano", "Bot"],
            "Cantidad": [human_messages, ai_messages],
        })

    # Notas adicionales para personalización futura
    st.sidebar.info("Puedes personalizar la descripción y el nombre del asistente para adaptarlo a tus necesidades.")


# Punto de entrada principal
if __name__ == '__main__':
    main()
