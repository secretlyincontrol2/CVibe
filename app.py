import streamlit as st
from streamlit_extras.colored_header import colored_header
from dotenv import load_dotenv
import os

# Import local modules
from components.sidebar import render_sidebar
from components.upload_section import render_upload_section
from components.job_preferences import render_job_preferences
from components.job_matches import render_job_matches
from components.about import render_about
from utils.session_state import initialize_session_state
from styles.custom_styles import apply_custom_styles

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="CVibe - Resume Analyzer & Job Matcher",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles
apply_custom_styles()

# Initialize session state variables
initialize_session_state()

# Render sidebar
render_sidebar()

# Main content
def main():
    # App header
    st.markdown("""
    <div class="main-header">
        <h1>CV<span class="accent">ibe</span></h1>
        <p class="subtitle">AI-Powered Resume Analysis & Job Matching</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display current step indicator
    steps = ["Upload Resume", "Set Preferences", "View Matches", "Apply"]
    current_step = st.session_state.get("current_step", 1)
    
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    
    for i, step in enumerate(steps):
        with cols[i]:
            if i + 1 < current_step:
                st.markdown(f"<div class='step completed'><div class='step-number'>{i+1}</div><div class='step-text'>{step}</div></div>", unsafe_allow_html=True)
            elif i + 1 == current_step:
                st.markdown(f"<div class='step current'><div class='step-number'>{i+1}</div><div class='step-text'>{step}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='step'><div class='step-number'>{i+1}</div><div class='step-text'>{step}</div></div>", unsafe_allow_html=True)
    
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    
    # Render the appropriate section based on current step
    if current_step == 1:
        render_upload_section()
    elif current_step == 2:
        render_job_preferences()
    elif current_step == 3:
        render_job_matches()
    elif current_step == 4:
        render_about()

if __name__ == "__main__":
    main()