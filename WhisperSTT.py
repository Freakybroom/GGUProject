import streamlit as st
import whisper
import os
import time
import tempfile
import subprocess

# Function to extract audio from video using ffmpeg
def extract_audio_from_video(video_path, audio_path):
    """Extract audio from video file using ffmpeg"""
    try:
        # Using ffmpeg to extract audio
        command = [
            "ffmpeg", 
            "-i", video_path, 
            "-q:a", "0", 
            "-map", "a", 
            "-vn", 
            audio_path,
            "-y"  # Overwrite output file if it exists
        ]
        
        # Run the command
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        
        # Check if the conversion was successful
        if process.returncode != 0:
            st.error(f"Error extracting audio: {stderr.decode()}")
            return False
        
        return True
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# App configuration
st.set_page_config(
    page_title="Whisper Speech-to-Text",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 Speech-to-Text with Whisper")
st.write("Convert speech to text using OpenAI's Whisper model")

# Create tabs for different features
tab1, tab2, tab3 = st.tabs(["Sample Audio", "Upload Audio", "Upload Video"])

with tab1:
    st.header("Sample Audio Transcription")
    
    # Path to the sample audio
    audio_path = r"C:\Users\Asus\Downloads\beta stage\Data\weather\whisper.cpp-master\samples\jfk.mp3"
    
    # Display audio player if file exists
    if os.path.exists(audio_path):
        st.audio(audio_path)
    else:
        st.error(f"Sample audio not found at: {audio_path}")
    
    # Model selection
    model_size = st.selectbox(
        "Select Whisper Model Size",
        ["tiny", "base", "small", "medium", "large"],
        index=1  # Default to "base"
    )
    
    if st.button("Transcribe Sample Audio"):
        if not os.path.exists(audio_path):
            st.error("Sample audio file not found.")
        else:
            # Show loading spinner while processing
            with st.spinner(f"Transcribing with {model_size} model... This may take a moment."):
                start_time = time.time()
                
                # Load the selected model
                model = whisper.load_model(model_size)
                
                # Run transcription
                result = model.transcribe(audio_path)
                
                # Calculate elapsed time
                elapsed = time.time() - start_time
                
                # Display success message
                st.success(f"✅ Transcription completed in {elapsed:.2f} seconds")
                
                # Display the complete transcription
                st.subheader("Transcription")
                st.text_area("Full Text", result["text"], height=150)
                
                # Display segments with timestamps
                st.subheader("Segments with Timestamps")
                for segment in result["segments"]:
                    st.markdown(f"**[{segment['start']:.2f}s - {segment['end']:.2f}s]** {segment['text']}")

with tab2:
    st.header("Upload Your Audio")
    
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a", "ogg"])
    
    if uploaded_file is not None:
        # Display uploaded audio
        st.audio(uploaded_file)
        
        # Save the uploaded file temporarily
        with open("temp_audio.mp3", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Model selection
        model_size = st.selectbox(
            "Select Whisper Model Size",
            ["tiny", "base", "small", "medium", "large"],
            index=1,  # Default to "base"
            key="upload_model_size"
        )
        
        if st.button("Transcribe Uploaded Audio"):
            # Show loading spinner while processing
            with st.spinner(f"Transcribing with {model_size} model... This may take a moment."):
                start_time = time.time()
                
                # Load the selected model
                model = whisper.load_model(model_size)
                
                # Run transcription
                result = model.transcribe("temp_audio.mp3")
                
                # Calculate elapsed time
                elapsed = time.time() - start_time
                
                # Display success message
                st.success(f"✅ Transcription completed in {elapsed:.2f} seconds")
                
                # Display the complete transcription
                st.subheader("Transcription")
                transcription = result["text"]
                st.text_area("Full Text", transcription, height=150)
                
                # Add download button
                st.download_button(
                    "Download Transcription",
                    transcription,
                    file_name="transcription.txt",
                    mime="text/plain"
                )
                
                # Display segments with timestamps
                st.subheader("Segments with Timestamps")
                for segment in result["segments"]:
                    st.markdown(f"**[{segment['start']:.2f}s - {segment['end']:.2f}s]** {segment['text']}")
            
            # Clean up the temporary file
            if os.path.exists("temp_audio.mp3"):
                os.remove("temp_audio.mp3")

with tab3:
    st.header("Video to Text")
    st.write("Upload a video file to extract audio and transcribe it")
    
    # File uploader for videos
    video_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv", "wmv"])
    
    if video_file is not None:
        # Display the uploaded video
        st.video(video_file)
        
        # Create temporary files for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(video_file.name)[1]) as video_temp:
            video_temp.write(video_file.getvalue())
            video_temp_path = video_temp.name
        
        audio_temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        
        # Model selection
        model_size = st.selectbox(
            "Select Whisper Model Size",
            ["tiny", "base", "small", "medium", "large"],
            index=1,  # Default to "base"
            key="video_model_size"
        )
        
        # Process button
        if st.button("Extract Audio and Transcribe"):
            try:
                # Step 1: Extract audio from video
                with st.spinner("Extracting audio from video..."):
                    if not extract_audio_from_video(video_temp_path, audio_temp_path):
                        st.error("Failed to extract audio from the video file.")
                        # Clean up temporary files
                        os.unlink(video_temp_path)
                        if os.path.exists(audio_temp_path):
                            os.unlink(audio_temp_path)
                        st.stop()
                    
                    st.success("Audio extracted successfully!")
                
                # Step 2: Transcribe the audio
                with st.spinner(f"Transcribing with {model_size} model... This may take a moment."):
                    start_time = time.time()
                    
                    # Load the selected model
                    model = whisper.load_model(model_size)
                    
                    # Run transcription
                    result = model.transcribe(audio_temp_path)
                    
                    # Calculate elapsed time
                    elapsed = time.time() - start_time
                    
                    # Display success message
                    st.success(f"✅ Transcription completed in {elapsed:.2f} seconds")
                
                # Display the complete transcription
                st.subheader("Transcription")
                transcription = result["text"]
                st.text_area("Full Text", transcription, height=150)
                
                # Add download button
                st.download_button(
                    "Download Transcription",
                    transcription,
                    file_name=f"{os.path.splitext(video_file.name)[0]}_transcription.txt",
                    mime="text/plain"
                )
                
                # Display segments with timestamps
                st.subheader("Segments with Timestamps")
                for segment in result["segments"]:
                    st.markdown(f"**[{segment['start']:.2f}s - {segment['end']:.2f}s]** {segment['text']}")
                
                # Option to download the extracted audio
                with open(audio_temp_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button(
                    "Download Extracted Audio",
                    audio_bytes,
                    file_name=f"{os.path.splitext(video_file.name)[0]}_audio.mp3",
                    mime="audio/mp3"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            finally:
                # Clean up temporary files
                if os.path.exists(video_temp_path):
                    os.unlink(video_temp_path)
                if os.path.exists(audio_temp_path):
                    os.unlink(audio_temp_path)

# Function to extract audio from video using ffmpeg
def extract_audio_from_video(video_path, audio_path):
    """Extract audio from video file using ffmpeg"""
    try:
        # Using ffmpeg to extract audio
        command = [
            "ffmpeg", 
            "-i", video_path, 
            "-q:a", "0", 
            "-map", "a", 
            "-vn", 
            audio_path,
            "-y"  # Overwrite output file if it exists
        ]
        
        # Run the command
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        
        # Check if the conversion was successful
        if process.returncode != 0:
            st.error(f"Error extracting audio: {stderr.decode()}")
            return False
        
        return True
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# Add information in the sidebar
st.sidebar.title("About")
st.sidebar.info(
    """
    This app uses [OpenAI's Whisper](https://github.com/openai/whisper) model for speech recognition.
    
    Whisper is an automatic speech recognition (ASR) system trained on 680,000 hours of multilingual and multitask supervised data.
    
    For video files, the app extracts audio using FFmpeg before processing with Whisper.
    """
)

# Display model information
st.sidebar.title("Model Information")
st.sidebar.markdown(
    """
    | Model | Parameters | English-only | Multilingual | Required VRAM | Relative speed |
    |-------|------------|--------------|--------------|---------------|----------------|
    | tiny  | 39 M       | tiny.en      | tiny         | ~1 GB         | ~32x           |
    | base  | 74 M       | base.en      | base         | ~1 GB         | ~16x           |
    | small | 244 M      | small.en     | small        | ~2 GB         | ~6x            |
    | medium| 769 M      | medium.en    | medium       | ~5 GB         | ~2x            |
    | large | 1550 M     | N/A          | large        | ~10 GB        | 1x             |
    """
)