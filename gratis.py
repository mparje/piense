import streamlit as st
import whisper
import openai
import streamlit_webrtc as webrtc
openai.api_key = "TU_API_KEY_DE_OPENAI_AQUI"  # Reemplaza esto con tu propia clave API de OpenAI
model_engine = "text-davinci-003"

# Crear la página de Streamlit
def main():
    st.title("Transcripción y ordenamiento de notas de voz")
    
    # Agregar la opción para grabar audio en la web
    webrtc_stream = webrtc.AudioRecorder(
        device=webrtc.RecordingDevice.DEFAULT,
        sample_rate=16000,
        channels=1,
    )
    recording = st.checkbox("Comenzar a grabar")
    if recording:
        webrtc_stream.recording = True
    else:
        webrtc_stream.recording = False
    
    # Si se graba el audio, transcribirlo usando Whisper
    if webrtc_stream.audio_bytes:
        with st.spinner("Transcribiendo el audio..."):
            text = whisper.transcribe_bytes(webrtc_stream.audio_bytes)
        st.success("La transcripción se ha completado correctamente.")
        
        # Ordenar las notas de voz usando el modelo de OpenAI
        with st.spinner("Ordenando las notas de voz..."):
            sorted_text = openai.Completion.create(
                engine=model_engine,
                prompt=text,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            ).choices[0].text
        
        # Mostrar las notas de voz transcritas y ordenadas en la página
        st.header("Notas de voz transcritas y ordenadas:")
        st.write(sorted_text)
    
    # Mostrar la opción de grabación de audio en la web en la página
    st.subheader("Grabar audio en la web:")
    webrtc_stream
    
if __name__ == "__main__":
    main()
