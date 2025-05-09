import streamlit as st
from utils.session_state import go_back

def render_about():
    """Render the about page with saved jobs summary"""
    st.markdown("## Your Saved Jobs")
    
    saved_jobs = st.session_state.get("saved_jobs", [])
    
    if not saved_jobs:
        st.warning("You haven't saved any jobs yet.")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("← Back to Job Matches", use_container_width=True):
                go_back()
                st.rerun()
        return
    
    st.markdown(f"You have saved **{len(saved_jobs)}** jobs. You can apply to them below or access them anytime from the sidebar.")
    
    # Display saved jobs
    for i, job in enumerate(saved_jobs):
        with st.expander(f"{job['title']} at {job['company']} - {job['match_score']}% Match"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Location:** {job['location']}")
                st.markdown(f"**Salary:** {job['salary']}")
                
                # Required skills with indicator of which ones match the resume
                st.markdown("**Required Skills:**")
                user_skills = set(st.session_state.resume_data.get("skills", []))
                
                skills_html = ""
                for skill in job["required_skills"]:
                    if skill.lower() in [s.lower() for s in user_skills]:
                        skills_html += f'<span class="skill match">{skill}</span>'
                    else:
                        skills_html += f'<span class="skill">{skill}</span>'
                
                st.markdown(f'<div class="skills-container">{skills_html}</div>', unsafe_allow_html=True)
                
                st.markdown("**Job Description:**")
                st.markdown(job["description"])
            
            with col2:
                if st.button("Apply Now", key=f"apply_saved_{i}", type="primary"):
                    st.markdown(f"<a href='{job['apply_url']}' target='_blank'>Apply on Company Website</a>", unsafe_allow_html=True)
                
                if st.button("Remove", key=f"remove_saved_{i}"):
                    st.session_state.saved_jobs.pop(i)
                    st.success("Job removed from saved list.")
                    st.rerun()
    
    # Next steps section
    st.markdown("---")
    st.markdown("## Next Steps")
    st.markdown("""
    Now that you've identified potential job matches, here are some tips for your applications:
    
    1. **Customize your resume** for each application to highlight relevant skills
    2. **Research the companies** to understand their culture and values
    3. **Prepare for interviews** by practicing common questions
    4. **Follow up** after applying to show your interest
    """)
    
    # Navigation
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back to Job Matches", use_container_width=True):
            go_back()
            st.rerun()
    
    with col2:
        if st.button("Start New Search", type="primary", use_container_width=True):
            st.session_state.current_step = 1
            st.session_state.resume_text = None
            st.session_state.resume_data = None
            st.session_state.job_matches = []
            st.rerun()