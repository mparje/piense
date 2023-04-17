import streamlit as st
import openai
import requests
import base64

# Configurar la clave de la API de OpenAI
api_key = st.sidebar.text_input("Ingrese su clave de la API de OpenAI", type="password")

if not api_key:
    st.warning("Por favor ingrese una clave de API válida para continuar.")
else:
    openai.api_key = api_key


# Configuración de la página
st.set_page_config(
    page_title="Grabador y ordenador de notas de voz",
    page_icon=":microphone:",
    layout="wide"
)

# Título de la página
st.title("Grabador y ordenador de notas de voz")

# Función para transcribir con Whisper
def transcribe_audio(audio_file):
    # URL de la API de Whisper
    url = "https://api.openai.com/v1/speech/transcriptions"

    # Carga el archivo de audio
    audio_data = audio_file.read()

    # Codifica el archivo de audio en base64
    encoded_audio = base64.b64encode(audio_data).decode("utf-8")

    # Parámetros de la solicitud HTTP
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "whisper-2021-10-05",
        "audio": encoded_audio
    }

    # Realiza la solicitud HTTP y obtiene la respuesta
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Decodifica la respuesta y obtiene la transcripción
    transcribed_text = json.loads(response.text)["text"]

    return transcribed_text

# Función para ordenar con Text-Davinci-003
def order_text(text):
    # URL de la API de Text-Davinci-003
    url = "https://api.openai.com/v1/engines/text-davinci-003/completions"

    # Parámetros de la solicitud HTTP
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    data = {
        "prompt": text,
        "temperature": 0.5,
        "max_tokens": 1024,
        "n": 1,
        "stop": "\n"
    }

    # Realiza la solicitud HTTP y obtiene la respuesta
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Decodifica la respuesta y obtiene la ordenación
    ordered_text = json.loads(response.text)["choices"][0]["text"]

    return ordered_text

# Interfaz de la aplicación
with st.sidebar:
    # Botón para grabar audio
    st.warning("Haga clic en el botón 'Grabar' para empezar a grabar")
    record_button = st.button("Grabar")

    # Botón para transcribir y ordenar
    st.warning("Haga clic en el botón 'Transcribir y ordenar' para generar las notas de voz")
    transcribe_button = st.button("Transcribir y ordenar")

# Grabación de audio
if record_button:
    # Configuración de la grabación de audio
    audio_bytes = st.audio_recorder(
        "Grabando audio",
        format="wav",
        start_recording=record_button,
        stop_recording=transcribe_button,
        key="audio"
    )

# Transcripción y ordenación de texto
if transcribe_button:
    # Transcripción con Whisper
    transcribed_text = transcribe_audio(audio_bytes)

    # Ordenación con Text-Davinci-003
    ordered_text = order_text(transcribed_text)

    # Muestra el resultado
    st.subheader("Notas de voz ordenadas")
    st.write(ordered_text)
