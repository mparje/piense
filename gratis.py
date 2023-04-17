import streamlit as st
import openai
import requests
from pydub import AudioSegment

# Configurar la clave de la API de OpenAI
api_key = st.sidebar.text_input("Ingrese su clave de la API de OpenAI", type="password")

if not api_key:
    st.warning("Por favor ingrese una clave de API válida para continuar.")
else:
    openai.api_key = api_key

    
    


# Función para transcribir el audio usando la API de Whisper de OpenAI
def transcribe_audio(audio_file):
    # Convierte el archivo de audio a formato WAV
    audio = AudioSegment.from_file(audio_file, format="mp3")
    audio.export("audio.wav", format="wav")
    
    # Carga el archivo WAV
    with open("audio.wav", "rb") as f:
        audio_data = f.read()
    
    # Realiza la transcripción usando la API de Whisper de OpenAI
    response = requests.post(
        "https://api.openai.com/v1/engines/whisper-asr/transcribe",
        headers={
            "Content-Type": "audio/wav",
            "Authorization": f"Bearer {openai.api_key}",
        },
        data=audio_data,
    )
    
    # Devuelve la transcripción
    return response.json()["transcription"]

# Interfaz de Streamlit
st.title("Transcriptor de audio con Whisper de OpenAI")
st.write("Sube un archivo de audio y lo transcribiré usando la API de Whisper de OpenAI.")

uploaded_file = st.file_uploader("Elige un archivo de audio", type=["mp3", "wav"])
if uploaded_file is not None:
    with st.spinner("Transcribiendo el audio..."):
        transcription = transcribe_audio(uploaded_file)
    st.write("Transcripción:")
    st.write(transcription)
else:
    st.write("Por favor, sube un archivo de audio.")
