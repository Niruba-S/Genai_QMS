
from lyzr import VoiceBot
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import zipfile

load_dotenv()

vb = VoiceBot(api_key="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")
genai.configure(api_key=os.getenv('API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def upload():
    try:
        uploaded_file = st.file_uploader('Upload a zip file', type=["zip"])
        if uploaded_file is not None:
            return uploaded_file
        else:
            st.text("UPLOAD A FILE")
    except:
        pass
   
def extract_zip(file_path, extract_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            file_info.filename = os.path.basename(file_info.filename)
            zip_ref.extract(file_info, extract_path)
    
def transcribe(file):
    transcripts = []
    transcript = vb.transcribe(file)
    transcripts.append(transcript)
    return transcripts

def main():
    st.title("AUDIO ANALYZER")
    
    files = upload()
    bname = st.button("PROCESS")
    extract = r"C:\Users\amjat\Desktop\airlines voice\extracted"
    
    if bname:
        if files:
            extract_zip(files.name, extract)
            all_transcripts = []
            for file in os.listdir(extract):
                audio_file_path = os.path.join(extract, file)
                trans = transcribe(audio_file_path)
                all_transcripts.extend(trans)
            st.write("Transcriptions:")
            for trans in all_transcripts:
                st.write(trans)

if __name__ == "__main__":
    main()
