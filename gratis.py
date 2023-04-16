import streamlit as st
import openai
import requests


api_key = st.sidebar.text_input("Ingrese su clave de la API de OpenAI", type="password")

if not api_key:
    st.warning("Por favor ingrese una clave de API válida para continuar.")
else:
    openai.api_key = api_key
    # Continuar con el resto del código que utiliza la clave de API

# Función para transcribir audio usando Whisper
def transcribe_audio(audio_file):
    # Cargar el archivo de audio en memoria
    audio_data = audio_file.read()

    # Realizar una solicitud a la API de OpenAI para transcribir el audio
    response = requests.post(
        "https://api.openai.com/v1/engines/whisper-asr/deployed/transcribe",
        headers={
            "Content-Type": "audio/wav",
            "Authorization": f"Bearer {openai.api_key}",
        },
        data=audio_data,
    )

    # Extraer el texto transcrito de la respuesta
    transcribed_text = response.content.decode("utf-8")
    transcribed_text = json.loads(transcribed_text)["transcription"]

    return transcribed_text

# Función para ordenar notas usando text-davinci-003
def sort_notes(transcribed_text):
    prompt = f"Ordena las siguientes notas de manera coherente:\n{transcribed_text}\n"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    sorted_notes = response.choices[0].text.strip()

    return sorted_notes

# Diseño de la interfaz de usuario de Streamlit
st.title("Transcriptor y organizador de notas")

uploaded_file = st.file_uploader("Suba su archivo de audio", type=["wav", "mp3"])

if uploaded_file is not None:
    transcribed_text = transcribe_audio(uploaded_file)
    st.write("Texto transcrito:", transcribed_text)

    sorted_notes = sort_notes(transcribed_text)
    st.write("Notas ordenadas:", sorted_notes)
