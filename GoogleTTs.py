import streamlit as st

# IMPORTANT: set_page_config must be the FIRST Streamlit command
st.set_page_config(layout="wide", page_title="Advanced Text-to-Speech App")

from google.cloud import texttospeech
from google.cloud import speech
import io
import os
from docx import Document
from PyPDF2 import PdfReader
import requests  # Added for translation API

# --- Configuration & Setup ---

# Set path to your Google Cloud credentials JSON file
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "google_credentials.json")

# Check if the credentials file exists
if os.path.exists(CREDENTIALS_PATH):
    # Set environment variable to point to the JSON file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
    st.sidebar.success(f"Using Google Cloud credentials from: {CREDENTIALS_PATH}")
else:
    st.sidebar.warning(f"Credentials file not found at: {CREDENTIALS_PATH}")
    st.sidebar.info("Create a JSON file named 'google_credentials.json' in the same directory as this script with your Google Cloud service account credentials.")

# Fallback to environment variable if already set
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ and os.environ["GOOGLE_APPLICATION_CREDENTIALS"] != CREDENTIALS_PATH:
    st.sidebar.info(f"Using credentials from environment variable: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")


# Initialize TTS and STT clients
try:
    tts_client = texttospeech.TextToSpeechClient()
except Exception as e:
    st.error(f"Failed to initialize Google Cloud clients. Ensure authentication is set up correctly: {e}")
    st.stop()

# --- Voice Definitions ---
# These are examples. You should check the Google Cloud TTS documentation for the latest voice names and availability.
# https://cloud.google.com/text-to-speech/docs/voices

# Part (a) - English Voices
ENGLISH_VOICES_PART_A = {
    "Male": {
        "Male Variant 1 (Standard)": "en-US-Standard-D",
        "Male Variant 2 (WaveNet)": "en-US-Wavenet-D",
        "Male Variant 3 (Neural2)": "en-US-Neural2-J",
        "Male Variant 4 (Studio)": "en-US-Studio-M", # Studio voices might have different pricing/quotas
    },
    "Female": {
        "Female Variant 1 (Standard)": "en-US-Standard-C",
        "Female Variant 2 (WaveNet)": "en-US-Wavenet-F",
        "Female Variant 3 (Neural2)": "en-US-Neural2-H",
        "Female Variant 4 (Studio)": "en-US-Studio-O", # Studio voices might have different pricing/quotas
    }
}

# Part (b) - Multilingual Voices (Example set of 7 languages)
# Each language should have 2 male and 2 female voice names
MULTILINGUAL_VOICES_PART_B = {
    "English (US)": {
        "language_code": "en-US",
        "translate_code": "en",
        "Male": ["en-US-Wavenet-A", "en-US-Neural2-D"],
        "Female": ["en-US-Wavenet-E", "en-US-Neural2-F"]
    },
    "Spanish (Spain)": {
        "language_code": "es-ES",
        "translate_code": "es",
        "Male": ["es-ES-Wavenet-B", "es-ES-Neural2-D"],
        "Female": ["es-ES-Wavenet-A", "es-ES-Neural2-C"]
    },
    "French (France)": {
        "language_code": "fr-FR",
        "translate_code": "fr",
        "Male": ["fr-FR-Wavenet-B", "fr-FR-Neural2-D"],
        "Female": ["fr-FR-Wavenet-A", "fr-FR-Neural2-C"]
    },
    "German (Germany)": {
        "language_code": "de-DE",
        "translate_code": "de",
        "Male": ["de-DE-Wavenet-B", "de-DE-Neural2-D"],
        "Female": ["de-DE-Wavenet-A", "de-DE-Neural2-C"]
    },
    "Hindi (India)": {
        "language_code": "hi-IN",
        "translate_code": "hi",
        "Male": ["hi-IN-Wavenet-B", "hi-IN-Neural2-D"],
        "Female": ["hi-IN-Wavenet-A", "hi-IN-Neural2-C"]
    },
    "Japanese (Japan)": {
        "language_code": "ja-JP",
        "translate_code": "ja",
        "Male": ["ja-JP-Wavenet-C", "ja-JP-Neural2-D"], # Neural2 might not exist for all, WaveNet is common
        "Female": ["ja-JP-Wavenet-A", "ja-JP-Neural2-B"]
    },
    "Mandarin Chinese (CN)": {
        "language_code": "cmn-CN", # or cmn-Hans-CN for Simplified
        "translate_code": "zh",
        "Male": ["cmn-CN-Wavenet-B", "cmn-CN-Wavenet-D"], # Fewer Neural2 voices for cmn typically
        "Female": ["cmn-CN-Wavenet-A", "cmn-CN-Wavenet-C"]
    }
}

# --- Helper Functions ---

def synthesize_speech(text, voice_name, language_code, speaking_rate=1.0):
    """Synthesizes speech from text using Google Cloud TTS."""
    if not text:
        return None, "Input text is empty."

    input_text = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate
    )

    try:
        response = tts_client.synthesize_speech(
            request={"input": input_text, "voice": voice_params, "audio_config": audio_config}
        )
        return response.audio_content, None
    except Exception as e:
        return None, f"TTS API Error: {e}"

def translate_text(text, target_language):
    """Translates text to target language using Google Cloud Translation API."""
    if not text:
        return "", "Input text is empty."
    
    try:
        # Using a free translation API for demonstration
        # For production, use Google Cloud Translation API or another paid service
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": target_language,
            "dt": "t",
            "q": text
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # Parse the response to get translated text
            data = response.json()
            translated = ''.join([sentence[0] for sentence in data[0]])
            return translated, None
        else:
            return "", f"Translation API Error: {response.status_code}"
    except Exception as e:
        return "", f"Translation Error: {e}"

def extract_text_from_file(uploaded_file):
    """Extracts text from uploaded .txt, .docx, or .pdf file."""
    if uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".docx"):
        try:
            doc = Document(io.BytesIO(uploaded_file.read()))
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            st.error(f"Error reading DOCX: {e}")
            return ""
    elif uploaded_file.name.endswith(".pdf"):
        try:
            reader = PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            return ""
    else:
        st.warning("Unsupported file type. Please upload .txt, .docx, or .pdf")
        return ""

# --- Streamlit UI ---
st.title("🔊 Advanced Text-to-Speech Application")
st.markdown("Powered by Google Cloud AI")

tab1, tab2 = st.tabs(["Mono-lingual TTS (English)", "Multi-lingual TTS"])

# --- Part (a): Text to Speech with different audio (English) ---
with tab1:
    st.header("English Text-to-Speech with Voice Variants")
    input_text_a = st.text_area("Enter text to synthesize (English):", height=150, key="text_a")

    col1a, col2a, col3a = st.columns(3)
    with col1a:
        gender_a = st.selectbox("Select Gender:", list(ENGLISH_VOICES_PART_A.keys()), key="gender_a")
    with col2a:
        if gender_a:
            voice_display_name_a = st.selectbox("Select Voice Variant:",
                                                list(ENGLISH_VOICES_PART_A[gender_a].keys()),
                                                key="voice_a")
            selected_voice_name_a = ENGLISH_VOICES_PART_A[gender_a][voice_display_name_a]
    with col3a:
        speed_a = st.slider("Select Audio Speed:", min_value=0.25, max_value=2.0, value=1.0, step=0.25, key="speed_a")

    if st.button("Synthesize Audio (English)", key="synth_a"):
        if input_text_a and selected_voice_name_a:
            with st.spinner("Generating audio..."):
                audio_content_a, error_a = synthesize_speech(input_text_a, selected_voice_name_a, "en-US", speed_a)
                if error_a:
                    st.error(error_a)
                elif audio_content_a:
                    st.audio(audio_content_a, format="audio/mp3")
                    st.download_button(
                        label="Download Audio",
                        data=audio_content_a,
                        file_name=f"english_speech_{selected_voice_name_a.replace('/', '_')}.mp3",
                        mime="audio/mp3"
                    )
        else:
            st.warning("Please enter text and select a voice.")

# --- Part (b): Text to Speech with Multilingual Option ---
with tab2:
    st.header("Multilingual Text-to-Speech")
    
    input_method_b = st.radio("Select Input Method:", ("Type Text", "Upload File"), key="input_method_b", horizontal=True)
    final_text_b = ""
    original_text_b = ""
    is_translated = False

    if input_method_b == "Type Text":
        original_text_b = st.text_area("Enter text to synthesize:", height=150, key="text_b_typed")
        final_text_b = original_text_b
    elif input_method_b == "Upload File":
        uploaded_file_b = st.file_uploader("Upload a text file (.txt, .docx, .pdf):", type=["txt", "docx", "pdf"], key="file_b")
        if uploaded_file_b:
            with st.spinner("Extracting text from file..."):
                original_text_b = extract_text_from_file(uploaded_file_b)
                final_text_b = original_text_b
                if original_text_b:
                    st.text_area("Extracted Text:", value=original_text_b, height=150, key="extracted_text_b", disabled=True)
                else:
                    st.warning("Could not extract text from the file or file is empty.")

    st.subheader("Language and Voice Selection")
    col1b, col2b, col3b = st.columns(3)

    with col1b:
        selected_language_display_name_b = st.selectbox("Select Language:", list(MULTILINGUAL_VOICES_PART_B.keys()), key="lang_b")
        language_details_b = MULTILINGUAL_VOICES_PART_B[selected_language_display_name_b]
        language_code_b = language_details_b["language_code"]
        translate_code_b = language_details_b["translate_code"]

    with col2b:
        gender_b = st.selectbox("Select Gender:", ["Male", "Female"], key="gender_b")
    
    with col3b:
        if gender_b and language_details_b[gender_b]:
            # Create display names for variants
            voice_options_b = {f"{gender_b} Variant {i+1} ({v.split('-')[-1]})": v
                              for i, v in enumerate(language_details_b[gender_b])}
            selected_voice_display_name_b = st.selectbox("Select Voice Variant:",
                                                       list(voice_options_b.keys()),
                                                       key="voice_b")
            selected_voice_name_b = voice_options_b[selected_voice_display_name_b]
        else:
            st.warning(f"No {gender_b} voices defined for {selected_language_display_name_b}.")
            selected_voice_name_b = None

    # Add translation option
    col1c, col2c = st.columns(2)
    with col1c:
        translate_option = st.checkbox("Translate text before synthesis", key="translate_option")
    
    with col2c:
        speed_b = st.slider("Select Audio Speed:", min_value=0.25, max_value=2.0, value=1.0, step=0.25, key="speed_b")
    
    # Add translate button
    if translate_option and original_text_b:
        if st.button("Translate Text", key="translate_btn"):
            with st.spinner(f"Translating text to {selected_language_display_name_b}..."):
                translated_text, error_trans = translate_text(original_text_b, translate_code_b)
                if error_trans:
                    st.error(error_trans)
                else:
                    final_text_b = translated_text
                    is_translated = True
                    st.text_area("Translated Text:", value=final_text_b, height=150, key="translated_text_b")

    # Display the text to be synthesized
    if is_translated:
        st.info("Synthesis will use the translated text shown above.")
    
    if st.button("Synthesize Multilingual Audio", key="synth_b"):
        if final_text_b and selected_voice_name_b and language_code_b:
            with st.spinner(f"Generating audio in {selected_language_display_name_b}..."):
                audio_content_b, error_b = synthesize_speech(final_text_b, selected_voice_name_b, language_code_b, speed_b)
                if error_b:
                    st.error(error_b)
                elif audio_content_b:
                    st.audio(audio_content_b, format="audio/mp3")
                    st.download_button(
                        label="Download Audio",
                        data=audio_content_b,
                        file_name=f"{language_code_b}_speech_{selected_voice_name_b.replace('/', '_')}.mp3",
                        mime="audio/mp3"
                    )
        elif not final_text_b:
            st.warning("Please provide text (type or upload).")
        elif not selected_voice_name_b:
            st.warning("Please select a valid voice for the chosen language and gender.")

st.markdown("---")
st.markdown("To use this app, ensure your Google Cloud credentials are set up.")
st.markdown("For local development, set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.")
st.markdown("For Streamlit Cloud deployment, add your GCP service account JSON content to Streamlit Secrets with the key `GOOGLE_APPLICATION_CREDENTIALS_JSON`.")
