import streamlit as st
import openai
import requests
from io import BytesIO

# Set OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Set Streamlit app title and description
st.set_page_config(page_title="Voice-to-Text and Text Generation", page_icon=":microphone:", layout="wide")
st.title("Voice-to-Text and Text Generation")
st.write("This app transcribes your voice and generates a well-written text based on your transcription.")

# Create a file uploader for audio files
uploaded_file = st.file_uploader("Upload an audio file (.wav or .mp3)", type=["wav", "mp3"])

# Create a text input for prompt
prompt = st.text_input("Enter a prompt for the text generation:")

# Define a function to transcribe voice using Whisper API
def transcribe_voice(audio_file):
    response = requests.post(
        "https://api.openai.com/v1/whisper/recognize",
        headers={"Authorization": f"Bearer {openai.api_key}"},
        data=audio_file,
    )
    if response.ok:
        return response.json()["text"]
    else:
        return None

# Define a function to generate text using GPT-3
def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    if response.choices:
        return response.choices[0].text
    else:
        return None

# Create a button to start transcription and text generation
if st.button("Generate Text"):
    # Check if audio file and prompt are provided
    if uploaded_file and prompt:
        # Transcribe voice using Whisper API
        st.write("Transcribing your voice...")
        audio_file = uploaded_file.read()
        audio_bytes = BytesIO(audio_file)
        transcription = transcribe_voice(audio_bytes)
        if transcription:
            st.write(f"Transcription: {transcription}")
            # Generate text using GPT-3
            st.write("Generating text...")
            text = generate_text(prompt + " " + transcription)
            if text:
                st.write(f"Generated Text: {text}")
            else:
                st.error("Failed to generate text.")
        else:
            st.error("Failed to transcribe voice.")
    else:
        st.warning("Please upload an audio file and enter a prompt for text generation.")
