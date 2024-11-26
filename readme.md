# README - Chat con Llama 3.1 utilizando Ollama y LangChain

Este proyecto utiliza **Streamlit**, **Ollama** y **LangChain** para crear un asistente virtual configurable que puede responder a preguntas y brindar soporte técnico en tiempo real.

---

## Requisitos

1. **Python 3.9 o superior**.
2. **Ollama** instalado para manejar el modelo de lenguaje.
3. Dependencias adicionales: `streamlit`, `langchain-core`, `langchain-community`.

---

## Instalación de dependencias

### 1. Clonar el repositorio
```bash
$ git clone <url-del-repositorio>
$ cd <nombre-del-directorio>
```

### 2. Crear un entorno virtual
```bash
$ python -m venv .venv
$ source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar las dependencias necesarias
```bash
$ pip install streamlit langchain-core langchain-community
```

---

## Instalación y configuración de Ollama

Ollama es una herramienta para manejar modelos de lenguaje como Llama 3.1 de manera local.

### 1. Descargar e instalar Ollama
- Ve al sitio oficial de Ollama: [https://ollama.com](https://ollama.com).
- Descarga el instalador correspondiente a tu sistema operativo.
- Sigue las instrucciones de instalación.

### 2. Verificar la instalación
Ejecuta el siguiente comando para verificar que Ollama esté instalado correctamente:
```bash
$ ollama list
```
Esto mostrará los modelos disponibles.

### 3. Descargar el modelo de Llama 3.1
Para descargar el modelo necesario, ejecuta:
```bash
$ ollama pull llama3.1:latest
```
Este comando asegurará que el modelo Llama 3.1 esté disponible localmente.

---

## Configuración del proyecto

### 1. Personalizar el asistente virtual
En la barra lateral de la aplicación Streamlit:

- **Nombre del asistente virtual**: Cambia el nombre del asistente según tus necesidades.
- **Descripción**: Personaliza la descripción del asistente para ajustar su comportamiento y tono de respuesta.

### 2. Configuración del historial de chat
El historial del chat se almacena en `st.session_state`. Puedes reiniciarlo en cualquier momento cerrando y volviendo a abrir la aplicación.

---

## Ejecución del proyecto

### 1. Inicia la aplicación
Ejecuta el siguiente comando para iniciar la aplicación:
```bash
$ streamlit run app.py
```

### 2. Interactúa con el asistente virtual
1. **Escribe una pregunta o consulta** en el campo de entrada.
2. Haz clic en el botón **Enviar** para obtener una respuesta.
3. Visualiza el historial de chat interactivo en la misma ventana.

### 3. Termina la interacción
Para finalizar el chat, escribe "Adiós". El sistema detendrá el procesamiento.

---

## Personalización adicional

### 1. Ajustar el modelo de lenguaje
El modelo se configura automáticamente para usar **Llama 3.1**. Puedes cambiar el modelo especificando uno diferente en esta línea del código:
```python
llm = Ollama(model="nombre_del_modelo")
```

### 2. Modificar el prompt del asistente
El comportamiento del asistente se controla mediante el siguiente prompt:
```python
prompt_default = f"""Eres un asistente virtual llamado {bot_name}, especializado en soporte técnico de nivel 1. Respondes de forma simple y clara, y realizas preguntas relevantes para recopilar más detalles del problema del usuario."""
```
Ajusta el contenido del prompt para adaptarlo a casos de uso específicos.

### 3. Integrar estadísticas del chat
La aplicación incluye un análisis básico de la interacción entre el usuario y el bot. Esto se puede personalizar o ampliar según las métricas deseadas.

---

## Recursos adicionales

- **Documentación de Ollama**: [https://ollama.com/docs](https://ollama.com/docs)
- **Documentación de LangChain**: [https://docs.langchain.com/](https://docs.langchain.com/)
- **Documentación de Streamlit**: [https://docs.streamlit.io/](https://docs.streamlit.io/)
google colab https://colab.research.google.com/drive/10dTQf3q1rjT_GqUfRMCyQwz9bV5ycjmf?usp=sharing
- 
---

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.