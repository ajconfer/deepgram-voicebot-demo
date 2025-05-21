
import streamlit as st
import requests
import os

# Set API keys (replace these in your hosted environment)
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.title("🎤 VoiceBot Assistant (Deepgram + GPT-4)")
st.write("Upload a voice message simulating a customer support query. We'll transcribe it with Deepgram and reply using GPT-4.")

uploaded_file = st.file_uploader("Upload your voice question (WAV/MP3)", type=["wav", "mp3"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")
    with st.spinner("Transcribing with Deepgram..."):
        response = requests.post(
            "https://api.deepgram.com/v1/listen",
            headers={
                "Authorization": f"Token {DEEPGRAM_API_KEY}",
                "Content-Type": uploaded_file.type
            },
            data=uploaded_file
        )

        if response.status_code != 200:
            st.error("Transcription failed: " + response.text)
        else:
            transcript = response.json()["results"]["channels"][0]["alternatives"][0]["transcript"]
            st.success("Transcription Complete!")
            st.markdown(f"**Transcript:** {transcript}")

            with st.spinner("Generating response..."):
                prompt = f"You are a helpful contact center AI assistant. A customer just said: '{transcript}'. How should you respond?"

                openai_response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.5
                    }
                )

                if openai_response.status_code != 200:
                    st.error("OpenAI API failed: " + openai_response.text)
                else:
                    reply = openai_response.json()["choices"][0]["message"]["content"]
                    st.markdown(f"**VoiceBot Reply:** {reply}")
