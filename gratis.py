import streamlit as st
import openai
import requests
import base64
from pydub import AudioSegment
from io import BytesIO

# Configurar la clave de la API de OpenAI
api_key = st.sidebar.text_input("Ingrese su clave de la API de OpenAI", type="password")

if not api_key:
    st.warning("Por favor ingrese una clave de API válida para continuar.")
else:
    openai.api_key = api_key



# Configura tu clave API de OpenAI
openai.api_key = "tu_clave_api"

# Función para transcribir el audio usando Whisper ASR
def transcribe_audio(audio_file):
    # Convierte el archivo de audio a formato WAV
    audio = AudioSegment.from_file(audio_file, format="mp3")
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export("audio.wav", format="wav")
    
    # Carga el archivo de audio en formato WAV
    with open("audio.wav", "rb") as f:
        audio_data = f.read()
    
    # Realiza la transcripción usando la API de OpenAI
    response = openai.Audio.create(
        audio=audio_data,
        model="whisper-asr",
        sample_rate=16000,
        format="wav",
        language="es",
    )
    
    # Devuelve la transcripción
    return response["choices"][0]["text"]

# Interfaz de Streamlit
st.title("Transcriptor de audio usando Whisper ASR")
st.write("Esta aplicación transcribe grabaciones de audio utilizando el modelo Whisper ASR de OpenAI.")

uploaded_file = st.file_uploader("Sube un archivo de audio en formato MP3", type=["mp3"])
if uploaded_file is not None:
    st.write("Archivo de audio cargado. Transcribiendo...")
    try:
        transcription = transcribe_audio(uploaded_file)
        st.write("Transcripción:")
        st.write(transcription)
    except Exception as e:
        st.write("Error al transcribir el archivo de audio.")
        st.write(str(e))
