from io import BytesIO
import numpy as np
import soundfile as sf
import speech_recognition as sr
import openai
import sys
import streamlit as st

# Configurar la clave de la API de OpenAI
api_key = st.sidebar.text_input("Ingrese su clave de la API de OpenAI", type="password")

if not api_key:
    st.warning("Por favor ingrese una clave de API válida para continuar.")
else:
    openai.api_key = api_key

    
    



device = 2
model = whisper.load_model("small")
recognizer = sr.Recognizer()

st.title("Transcripción de Voz con OpenAI y Streamlit")

while True:
    st.write("Habla en el micrófono para empezar a transcribir:")
    with sr.Microphone(device_index=device, sample_rate=16_000) as source:
        audio = recognizer.listen(source)

    wav_bytes = audio.get_wav_data()
    wav_stream = BytesIO(wav_bytes)
    audio_array, sampling_rate = sf.read(wav_stream)
    audio_fp32 = audio_array.astype(np.float32)

    result = model.transcribe(audio_fp32, fp16=False)
    st.write(f"Transcripción: {result['text']}")
