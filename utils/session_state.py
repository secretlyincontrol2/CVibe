import streamlit as st

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if "current_step" not in st.session_state:
        st.session_state.current_step = 1
    
    if "resume_text" not in st.session_state:
        st.session_state.resume_text = None
    
    if "resume_data" not in st.session_state:
        st.session_state.resume_data = None
    
    if "parsed_skills" not in st.session_state:
        st.session_state.parsed_skills = []
    
    if "parsed_experience" not in st.session_state:
        st.session_state.parsed_experience = []
    
    if "parsed_education" not in st.session_state:
        st.session_state.parsed_education = []
    
    if "job_matches" not in st.session_state:
        st.session_state.job_matches = []
    
    if "location_preference" not in st.session_state:
        st.session_state.location_preference = "Any"
    
    if "experience_level" not in st.session_state:
        st.session_state.experience_level = "Any"
    
    if "job_type" not in st.session_state:
        st.session_state.job_type = "Full-time"
    
    if "industry_preference" not in st.session_state:
        st.session_state.industry_preference = "Any"
    
    if "saved_jobs" not in st.session_state:
        st.session_state.saved_jobs = []

def advance_step():
    """Advance to the next step"""
    st.session_state.current_step += 1

def go_back():
    """Go back to the previous step"""
    st.session_state.current_step -= 1

def reset_state():
    """Reset the app state"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()