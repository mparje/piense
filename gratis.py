import openai
import pyttsx3
import speech_recognition as sr
import whisper
import json 
import streamlit as st
import os

# openai
openai.api_key = os.getenv("API_KEY")
model = whisper.load_model('base')
engine = pyttsx3.init()

# set engine
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')

r = sr.Recognizer()
mic = sr.Microphone(device_index=2)


def run_bot():
    conversation = ""
    user_name = "Ayla"
    bot_name = "Bot"

    while st.session_state.conversation_running:
        with mic as source:
            st.write("\nlistening...")
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
            with open('output.wav', 'wb') as f:
                f.write(audio.get_wav_data())
        st.write("no longer listening.\n")
        
        try:
            output = model.transcribe('output.wav', fp16=False)
            user_input = output['text']
            st.write("user input : " + user_input)
        except Exception as e :
            st.write(e)
            continue
        
        prompt = user_name + ": " + user_input + "\n" + bot_name+ ": "
        
        conversation += prompt
        
        response = openai.Completion.create(
                engine = "text-davinci-003",
                prompt = conversation,
                max_tokens = 1024,
                n = 1,
                stop=[user_name+":"],
                temperature=0.2,
            )
        response_str = response["choices"][0]["text"].replace("\n", "")
        response_str = response_str.split(user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]
        
        conversation += response_str + "\n"
        st.write(response_str)
        
        engine.say(response_str)
        engine.runAndWait()


def main():
    st.title("Voice-based chatbot")
    st.write("Press the start button to begin the conversation.")
    
    if "conversation_running" not in st.session_state:
        st.session_state.conversation_running = False

    if not st.session_state.conversation_running:
        if st.button("Start"):
            st.session_state.conversation_running = True
            run_bot()
    else:
        if st.button("Stop"):
            st.session_state.conversation_running = False
            engine.stop()


if __name__ == "__main__":
    main()
