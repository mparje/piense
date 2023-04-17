import streamlit as st
import openai
import pyaudio
import wave

# Configurar la clave de la API de OpenAI
api_key = st.sidebar.text_input("Ingrese su clave de la API de OpenAI", type="password")

if not api_key:
    st.warning("Por favor ingrese una clave de API válida para continuar.")
else:
    openai.api_key = api_key

    
    




def record_voice():
    st.write("Presione el botón de abajo para comenzar a grabar")
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    frames = []
    try:
        while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    audio.terminate()

    sound_file = wave.open("Recording.wav", "wb")

    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()
    st.write("¡La grabación ha finalizado!")


def get_voice():
    st.write("Presione el botón de abajo para transcribir la grabación")
    openai.api_key = "API-KEY"
    audio_file = open("Recording.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    st.write("Transcripción de la grabación:")
    st.write(transcript)


# UI
st.title("Transcripción de Voz")

option = st.sidebar.selectbox("Seleccione una opción", ("Grabar voz", "Transcribir voz"))

if option == "Grabar voz":
    record_voice()
elif option == "Transcribir voz":
    get_voice()
