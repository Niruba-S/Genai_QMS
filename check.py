

import streamlit as st
import google.generativeai as genai
import logging
import assemblyai as aai  # Assuming you have AssemblyAI installed
from io import BytesIO

# Configure GenerativeAI and AssemblyAI (replace with your API keys)
# Configure GenerativeAI and AssemblyAI (replace with your API keys)
genai.configure(api_key="AIzaSyBxbqUnQvC5tc5YLX_5CVIC-d_vEmHb1Ss")
aai.settings.api_key = "4e36f069d21d46c481552d56b7bbbf87"


# GenerativeAI model and session state
model = genai.GenerativeModel('gemini-pro')
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Streamlit app layout
st.markdown("<h1 style='text-align: center; color:red;'>BAASHHA AI</h1>", unsafe_allow_html=True)
st.markdown("""<style>body { background-color: red; }</style>""", unsafe_allow_html=True)

def transcribe_audio(audio_file):
    # Read file content as bytes
    audio_bytes = audio_file.read()
    
    # Use AssemblyAI to transcribe audio
    transcript = aai.Transcriber().transcribe(audio_bytes)
    return transcript.text

def main():
    try:
        # User input (audio)
        uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])

        if uploaded_file is not None:
            # Transcribe uploaded audio
            transcript_text = transcribe_audio(uploaded_file)

            # Sentiment analysis using GenerativeAI
            response = model.sentiment(transcript_text)

            # Key phrase extraction using GenerativeAI
            key_phrases = model.key_phrases(transcript_text)

            # Check if the user's message is about terrorist organizations
            if "terrorist organization" in transcript_text.lower() or "designation" in transcript_text.lower():
                # Provide unambiguous answer
                st.write("The designation of terrorist organizations varies by government and international organizations. For specific information, please consult official sources such as government websites or international organizations' publications.")
            else:
                # Display sentiment analysis result
                st.write("Sentiment:", response.sentiment)
                st.write("Sentiment Score:", response.score)

                # Display key phrases
                st.write("Key Phrases:", key_phrases)

                # Generate response using GenerativeAI model
                response = model.generate_content(transcript_text)

                if response and hasattr(response, 'text'):
                    st.write(response.text)
                else:
                    st.warning("Failed to generate content. Please try again.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logging.error(f'Error: {str(e)}')

if __name__ == "__main__":
    main()
