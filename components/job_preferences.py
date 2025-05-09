import streamlit as st
from utils.session_state import advance_step, go_back

def render_job_preferences():
    """Render the job preferences selection section"""
    st.markdown("## Set Your Job Preferences")
    st.markdown("Customize your job search by setting your preferences below.")
    
    # Check if resume data exists
    if not st.session_state.get("resume_data"):
        st.error("No resume data found. Please upload your resume first.")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Back to Resume Upload", use_container_width=True):
                st.session_state.current_step = 1
                st.rerun()
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Location preference
        st.markdown("### Location Preference")
        location_options = ["Any", "Remote", "Hybrid", "Onsite"]
        location_icons = ["🌍", "🏠", "🏢", "🏙️"]
        
        location_type = st.radio(
            "Select your preferred work location:",
            options=location_options,
            index=location_options.index(st.session_state.get("location_preference", "Any")),
            format_func=lambda x: f"{location_icons[location_options.index(x)]} {x}",
            horizontal=True
        )
        st.session_state.location_preference = location_type
        
        # If not "Any", let the user specify a location
        if location_type in ["Hybrid", "Onsite"]:
            location = st.text_input(
                "Enter your preferred city/region:",
                value=st.session_state.get("location_city", "")
            )
            st.session_state.location_city = location
        
        # Experience level
        st.markdown("### Experience Level")
        experience_options = ["Any", "Entry Level", "Mid Level", "Senior", "Executive"]
        experience = st.select_slider(
            "Select your experience level:",
            options=experience_options,
            value=st.session_state.get("experience_level", "Any")
        )
        st.session_state.experience_level = experience
    
    with col2:
        # Job type
        st.markdown("### Job Type")
        job_type_options = ["Full-time", "Part-time", "Contract", "Internship", "Freelance"]
        job_type = st.selectbox(
            "Select job type:",
            options=job_type_options,
            index=job_type_options.index(st.session_state.get("job_type", "Full-time"))
        )
        st.session_state.job_type = job_type
        
        # Industry preference
        st.markdown("### Industry Preference")
        industry_options = [
            "Any", "Technology", "Finance", "Healthcare", "Education", 
            "Manufacturing", "Retail", "Media", "Government", "Non-profit"
        ]
        industry = st.selectbox(
            "Select preferred industry:",
            options=industry_options,
            index=industry_options.index(st.session_state.get("industry_preference", "Any"))
        )
        st.session_state.industry_preference = industry
        
        # Salary expectations (optional)
        st.markdown("### Salary Expectations (Optional)")
        min_salary = st.number_input(
            "Minimum salary ($):",
            min_value=0,
            max_value=1000000,
            value=st.session_state.get("min_salary", 0),
            step=5000
        )
        st.session_state.min_salary = min_salary
    
    # Skills customization
    st.markdown("### Skills")
    st.markdown("Review and customize the skills extracted from your resume:")
    
    if st.session_state.get("resume_data") and "skills" in st.session_state.resume_data:
        skills = st.session_state.resume_data["skills"]
        
        # Allow user to edit the skills
        skills_str = ", ".join(skills)
        edited_skills = st.text_area(
            "Edit your skills (comma-separated):",
            value=skills_str,
            height=100
        )
        
        # Update skills in session state
        if edited_skills:
            new_skills = [skill.strip() for skill in edited_skills.split(",") if skill.strip()]
            st.session_state.resume_data["skills"] = new_skills
    else:
        st.warning("No skills found in your resume. Add some skills to improve job matching.")
        skills_input = st.text_area(
            "Enter your skills (comma-separated):",
            height=100
        )
        if skills_input:
            skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]
            if "resume_data" not in st.session_state:
                st.session_state.resume_data = {}
            st.session_state.resume_data["skills"] = skills
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back", use_container_width=True):
            go_back()
            st.rerun()
    
    with col3:
        if st.button("Find Matching Jobs →", type="primary", use_container_width=True):
            # Gather preferences into a dictionary
            preferences = {
                "location_type": st.session_state.location_preference,
                "experience_level": st.session_state.experience_level,
                "job_type": st.session_state.job_type,
                "industry": st.session_state.industry_preference,
                "min_salary": st.session_state.min_salary
            }
            
            if st.session_state.location_preference in ["Hybrid", "Onsite"] and st.session_state.get("location_city"):
                preferences["location_city"] = st.session_state.location_city
            
            # Store preferences in session state
            st.session_state.job_preferences = preferences
            
            # Advance to next step
            advance_step()
            st.rerun()