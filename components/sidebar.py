import streamlit as st
from utils.session_state import reset_state
import os

# Ensure the directory exists
os.makedirs("assets/images", exist_ok=True)

def render_sidebar():
    """Render the sidebar with app information and options"""
    with st.sidebar:
        # Use a relative path for the image
        image_path = "assets/images/careerTech.jpg"
        
        # Check if the file exists before rendering
        if os.path.exists(image_path):
            st.image(image_path, width=300)
        else:
            st.error("Sidebar image not found. Please ensure the file exists at 'assets/images/careerTech.jpg'.")
        
        st.markdown("### About CVibe")
        st.markdown("""
        CVibe helps you optimize your job search by analyzing your resume and matching it with suitable job vacancies.
        
        **How it works:**
        - Upload your resume (PDF or DOCX)
        - Our AI parses your skills and experience
        - Set your job preferences
        - View matched job opportunities
        - Apply directly to positions that interest you
        - Save jobs to review later
        """)
        
        st.markdown("---")
        st.markdown("### Navigation")
        
        # Navigation buttons
        if st.button("⬅️ Start Over", key="btn_start_over"):
            reset_state()
            st.rerun()
        
        # Show step-specific navigation
        current_step = st.session_state.get("current_step", 1)
        
        if current_step > 1:
            if st.button("🔄 Upload New Resume", key="btn_new_resume"):
                st.session_state.current_step = 1
                st.session_state.resume_text = None
                st.session_state.resume_data = None
                st.rerun()
        
        if current_step > 2 and st.button("🔧 Change Preferences", key="btn_change_prefs"):
            st.session_state.current_step = 2
            st.rerun()
        
        if st.session_state.get("job_matches") and current_step > 2:
            if st.button("📝 View Job Matches", key="btn_view_matches"):
                st.session_state.current_step = 3
                st.rerun()
        
        st.markdown("---")
        
        # Saved jobs section
        saved_jobs = st.session_state.get("saved_jobs", [])
        st.markdown("### Saved Jobs")
        
        if not saved_jobs:
            st.markdown("No saved jobs yet!")
        else:
            for i, job in enumerate(saved_jobs):
                with st.expander(f"{job['title']} at {job['company']}"):
                    st.markdown(f"**Match Score:** {job['match_score']}%")
                    st.markdown(f"**Location:** {job['location']}")
                    st.markdown(f"**Salary:** {job['salary']}")
                    
                    if st.button("Apply Now", key=f"apply_{i}"):
                        st.markdown(f"[Apply on Company Website]({job['apply_url']})")
                    
                    if st.button("Remove", key=f"remove_{i}"):
                        st.session_state.saved_jobs.pop(i)
                        st.rerun()
        
        st.markdown("---")
        st.markdown("### Privacy Note")
        st.markdown("""
        Your resume data is used only for generating job matches and is not stored permanently.
        We value your privacy.
        """)