import streamlit as st
import time
from PIL import Image
import base64
import random

# Configure page settings
st.set_page_config(
    page_title="Voice & Text AI Suite",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check if a page is already set in session_state
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# Custom CSS for animations and styling
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;700;900&display=swap');
    
    * {font-family: 'Roboto', sans-serif;}
    
    .title {
        color: #1E88E5;
        font-size: 3.5rem !important;
        font-weight: 700;
        margin-bottom: 0;
        padding-bottom: 0;
        animation: fadeIn 1.5s ease-in-out;
    }
    
    .subtitle {
        color: #424242;
        font-size: 1.5rem !important;
        font-weight: 300;
        margin-top: 0;
        animation: slideIn 1.5s ease-in-out;
    }
    
    .card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeIn 1.5s ease-in-out;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
    }
    
    .card-title {
        color: #1E88E5;
        font-size: 1.5rem !important;
        font-weight: 500;
    }
    
    .card-text {
        color: #424242;
        font-size: 1rem !important;
    }
    
    .feature-icon {
        font-size: 2.5rem !important;
        margin-bottom: 15px;
        color: #1E88E5;
    }
    
    .button {
        background-color: #1E88E5;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    
    .button:hover {
        background-color: #1565C0;
    }
      .stApp {
        background-color: #2D3436;
        color: #FFFFFF;
    }
    
    .stTextInput > div > div > input {
        background-color: #3D4548;
        color: white;
    }
    
    .stSelectbox > div > div > select {
        background-color: #3D4548;
        color: white;
    }
    
    h1, h2, h3, h4 {
        color: #E0E0E0 !important;
    }
    
    .card {
        background-color: #3D4548;
    }
    
    .card-title {
        color: #64B5F6 !important;
    }
    
    .card-text {
        color: #E0E0E0 !important;
    }
    
    .footer {
        color: #BDBDBD;
    }
    
    @keyframes fadeIn {
        0% {opacity: 0;}
        100% {opacity: 1;}
    }
    
    @keyframes slideIn {
        0% {transform: translateY(20px); opacity: 0;}
        100% {transform: translateY(0); opacity: 1;}
    }
    
    .delayed-animation {
        opacity: 0;
        animation: fadeIn 1s ease-in-out forwards;
    }
    
    .delay-1 {animation-delay: 0.5s;}
    .delay-2 {animation-delay: 1s;}
    .delay-3 {animation-delay: 1.5s;}
    .delay-4 {animation-delay: 2s;}
    
    .floating {
        animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
        0% {transform: translateY(0px);}
        50% {transform: translateY(-10px);}
        100% {transform: translateY(0px);}
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {transform: scale(1);}
        50% {transform: scale(1.05);}
        100% {transform: scale(1);}
    }
    
    .footer {
        margin-top: 50px;
        text-align: center;
        color: #9E9E9E;
        font-size: 0.8rem;
        padding: 20px;
    }
    
    /* Loading animation */
    .loader {
        display: inline-block;
        width: 80px;
        height: 80px;
    }
    .loader:after {
        content: " ";
        display: block;
        width: 64px;
        height: 64px;
        margin: 8px;
        border-radius: 50%;
        border: 6px solid #1E88E5;
        border-color: #1E88E5 transparent #1E88E5 transparent;
        animation: loader 1.2s linear infinite;
    }
    @keyframes loader {
        0% {transform: rotate(0deg);}
        100% {transform: rotate(360deg);}
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Function to create a particle animation background with base64
def get_particle_animation_html():
    return """
    <div id="particles-js" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
    particlesJS('particles-js', {
        "particles": {
            "number": {
                "value": 80,
                "density": {
                    "enable": true,
                    "value_area": 800
                }
            },
            "color": {
                "value": "#1E88E5"
            },
            "shape": {
                "type": "circle",
                "stroke": {
                    "width": 0,
                    "color": "#000000"
                },
            },
            "opacity": {
                "value": 0.5,
                "random": false,
                "anim": {
                    "enable": false,
                    "speed": 1,
                    "opacity_min": 0.1,
                    "sync": false
                }
            },
            "size": {
                "value": 3,
                "random": true,
            },
            "line_linked": {
                "enable": true,
                "distance": 150,
                "color": "#1E88E5",
                "opacity": 0.4,
                "width": 1
            },
            "move": {
                "enable": true,
                "speed": 2,
                "direction": "none",
                "random": false,
                "straight": false,
                "out_mode": "out",
                "bounce": false,
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {
                    "enable": true,
                    "mode": "grab"
                },
                "onclick": {
                    "enable": true,
                    "mode": "push"
                },
                "resize": true
            },
            "modes": {
                "grab": {
                    "distance": 140,
                    "line_linked": {
                        "opacity": 1
                    }
                },
                "push": {
                    "particles_nb": 4
                },
            }
        },
        "retina_detect": true
    });
    </script>
    """

# Add particles.js animation
st.markdown(get_particle_animation_html(), unsafe_allow_html=True)

# Animated title and subtitle
st.markdown("<h1 class='title'>Voice & Text AI Suite</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Powered by Advanced Machine Learning</p>", unsafe_allow_html=True)

# Check if a page is already set in session_state for navigation
if st.session_state.get('page') != 'home':
    selected_page = st.session_state.get('page')
    st.session_state['page'] = 'home'  # Reset to prevent loops
    
    # We'll handle page navigation later in the script

# Add a session state check to handle page navigation
if st.session_state.get('page') != 'home':
    selected_page = st.session_state.get('page')
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pages_dir = os.path.join(script_dir, "pages")
    
    # Check which page to load
    if selected_page == "WhisperSTT" and os.path.exists(os.path.join(pages_dir, "WhisperSTT.py")):
        import sys
        sys.path.append(pages_dir)
        import WhisperSTT
        st.stop()
    elif selected_page == "GoogleTTS" and os.path.exists(os.path.join(pages_dir, "GoogleTTS.py")):
        import sys
        sys.path.append(pages_dir)
        import GoogleTTS
        st.stop()

# Simulated loading spinner for a more interactive effect
with st.spinner("Loading AI Models..."):
    progress_bar = st.progress(0)
    for percent_complete in range(0, 101, 5):
        time.sleep(0.05)
        progress_bar.progress(percent_complete)
    time.sleep(0.5)
    st.success("All models loaded successfully!")
    time.sleep(0.5)
    progress_bar.empty()

# Main content container
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# Create two columns for the features
col1, col2 = st.columns(2)

# Speech-to-Text feature card
with col1:
    st.markdown("""
    <div class='card delayed-animation delay-1'>
        <h2 class='card-title'>Speech-to-Text</h2>
        <p class='card-text'>Transform spoken language into written text with our advanced speech recognition technology.</p>
        <div style='text-align: center; margin-top: 20px;'>
            <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjJoZjRrZHlpZTNuY2RiaXN2eW8waWF5Z3N0bGRlMjlmZnVuaG92OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QAC7BXHGCcwxKQA7fg/giphy.gif" width="100" class="floating">
        </div>
        <p class='card-text'>
            <strong>Features:</strong>
            <ul>
                <li>Real-time speech recognition</li>
                <li>Support for multiple languages</li>
                <li>High accuracy with noise filtering</li>
                <li>Format and export transcriptions</li>
                <li>Process audio files or use microphone input</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Text-to-Speech feature card
with col2:
    st.markdown("""
    <div class='card delayed-animation delay-2'>
        <h2 class='card-title'>Text-to-Speech</h2>
        <p class='card-text'>Convert written text into natural-sounding speech using our state-of-the-art voice synthesis.</p>
        <div style='text-align: center; margin-top: 20px;'>
            <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWd3Y3d4NDM5cGVxc2Zna3h2ZXJjMHNkN2FxejQwNmlwZXNpaDl0bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/SvLk7h1JoYnkY0rvHF/giphy.gif" width="100" class="floating">
        </div>
        <p class='card-text'>
            <strong>Features:</strong>
            <ul>
                <li>Natural-sounding voices</li>
                <li>Multiple language support</li>
                <li>Control pitch, speed, and emphasis</li>
                <li>Choose from different voice types</li>
                <li>Download audio for offline use</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Tech stack section
st.markdown("<div class='card delayed-animation delay-3'>", unsafe_allow_html=True)
st.subheader("🧠 Powered by Advanced Technology")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.markdown("""
    <div style='text-align: center;'>
        <h3>AI Models</h3>
        <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExejd6MWl0amZ1aWlqdjkxMnAwZmdsZGpvNXcwYTcxODJwZ2dsYnR3ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l4FGlR7JsKUTMXGCY/giphy.gif" width="60" style="margin-bottom:10px;">
        <p>Utilizing state-of-the-art LLMs for natural language understanding and generation</p>
        <ul style='list-style-type: none; padding: 0;'>
            <li>✓ Google Cloud Speech API</li>
            <li>✓ OpenAI Whisper</li>
            <li>✓ Google Text-to-Speech</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tech_col2:
    st.markdown("""
    <div style='text-align: center;'>
        <h3>Data Processing</h3>
        <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeG96bGhzNHdnbjc0ZndsYzIwZjl1cmVsZDdkZDF1NGo3aTJiN3I0aiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPEqDGUULpEU0aQ/giphy.gif" width="60" style="margin-bottom:10px;">
        <p>Sophisticated algorithms for text and audio processing</p>
        <ul style='list-style-type: none; padding: 0;'>
            <li>✓ Real-time analysis</li>
            <li>✓ Multi-language support</li>
            <li>✓ Advanced formatting</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tech_col3:
    st.markdown("""
    <div style='text-align: center;'>
        <h3>Python Libraries</h3>
        <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHlvbXMyaGt0cDc3aWpieHo3bzZlZTk5M2RidG9jZGY4NmQ2cWptNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KAq5w47R9rmTuvWOWa/giphy.gif" width="60" style="margin-bottom:10px;">
        <p>Built with powerful open-source tools</p>
        <ul style='list-style-type: none; padding: 0;'>
            <li>✓ Streamlit</li>
            <li>✓ PyTorch</li>
            <li>✓ SoundFile</li>
            <li>✓ WebRTC</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Get started section with animated buttons
st.markdown("<div class='card delayed-animation delay-4'>", unsafe_allow_html=True)
st.subheader("🚀 Get Started")

# Create three columns for the buttons
btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    if st.button("Speech to Text", key="stt_button", use_container_width=True):
        # Navigate to WhisperSTT from pages section
        import os
        import sys
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pages_dir = os.path.join(script_dir, "pages")
        if os.path.exists(os.path.join(pages_dir, "WhisperSTT.py")):
            st.session_state["page"] = "WhisperSTT"
            st.rerun()
        else:
            st.error("WhisperSTT.py not found in pages directory")

with btn_col2:
    if st.button("Text to Speech", key="tts_button", use_container_width=True):
        # Navigate to GoogleTTS from pages section
        import os
        import sys
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pages_dir = os.path.join(script_dir, "pages")
        if os.path.exists(os.path.join(pages_dir, "GoogleTTS.py")):
            st.session_state["page"] = "GoogleTTS"
            st.rerun()
        else:
            st.error("GoogleTTS.py not found in pages directory")

with btn_col3:
    st.markdown("""
    <div style='text-align: center;'>
        <a href='/?page=about' target='_self'>
            <button class='button' style='width: 100%;'>
                About This App
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Interactive demo (randomly generated waveform to simulate audio)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🌊 Live Demo")

st.markdown("""    <div style='background-color: #1E2022; border-radius: 10px; padding: 20px; text-align: center;'>
    <div id='waveform' style='height: 100px; position: relative; overflow: hidden;'>
        <canvas id='waveCanvas' width='800' height='100'></canvas>
    </div>
</div>
<script>
    // Simple audio waveform animation
    const canvas = document.getElementById('waveCanvas');
    const ctx = canvas.getContext('2d');
    
    // Set canvas to parent width
    canvas.width = canvas.parentElement.offsetWidth;
    
    function drawWave() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
        
        const amplitude = 30;
        const frequency = 0.02;
        const speed = Date.now() * 0.005;
        
        ctx.moveTo(0, canvas.height / 2);
        
        for (let x = 0; x < canvas.width; x++) {
            let y = canvas.height / 2 + 
                    amplitude * Math.sin(x * frequency + speed) + 
                    amplitude * 0.5 * Math.sin(x * frequency * 2 + speed * 1.5) +
                    amplitude * 0.25 * Math.sin(x * frequency * 3 + speed * 0.5);
            
            ctx.lineTo(x, y);
        }
        
        ctx.strokeStyle = '#1E88E5';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        requestAnimationFrame(drawWave);
    }
    
    drawWave();
</script>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Footer with credits
st.markdown("""
<div class='footer'>
    <p>© 2025 Voice & Text AI Suite | Powered by Python & Streamlit | Created with ❤️ by AI Engineers</p>
    <p>Version 1.0.0 | Last Updated: May 2025</p>
</div>
""", unsafe_allow_html=True)

# Add some navigation in the sidebar
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose the app mode",
    ["Home", "Speech-to-Text", "Text-to-Speech", "About"])

st.sidebar.markdown("---")
st.sidebar.subheader("Settings")
st.sidebar.checkbox("Dark Mode", False)
st.sidebar.checkbox("High Quality Audio", True)
st.sidebar.checkbox("Save History", True)

st.sidebar.markdown("---")
st.sidebar.subheader("Resources")
st.sidebar.markdown("• [Documentation](https://example.com)")
st.sidebar.markdown("• [GitHub Repository](https://github.com)")
st.sidebar.markdown("• [Report an Issue](https://example.com/issues)")

# Handle navigation based on sidebar selection
if app_mode == "Speech-to-Text":
    # In a real app, you would use st.switch_page() for multi-page apps
    # or create a state management system for single-page apps
    st.session_state["page"] = "WhisperSTT"
    st.rerun()
elif app_mode == "Text-to-Speech":
    st.session_state["page"] = "GoogleTTS"
    st.rerun()
elif app_mode == "About":
    st.session_state["page"] = "about"
    st.rerun()
