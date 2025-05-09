import streamlit as st
from utils.job_matcher import match_jobs_with_ai
from utils.session_state import advance_step, go_back

def render_job_matches():
    """Render the job matches section"""
    st.markdown("## Your Job Matches")
    
    # Check if resume data and preferences exist
    if not st.session_state.get("resume_data"):
        st.error("No resume data found. Please upload your resume first.")
        if st.button("Back to Resume Upload"):
            st.session_state.current_step = 1
            st.rerun()
        return
    
    if not st.session_state.get("job_preferences"):
        st.error("No job preferences found. Please set your preferences first.")
        if st.button("Back to Job Preferences"):
            st.session_state.current_step = 2
            st.rerun()
        return
    
    # Get job matches if not already present
    if not st.session_state.get("job_matches"):
        with st.spinner("Finding your perfect job matches..."):
            job_matches = match_jobs_with_ai(
                st.session_state.resume_data,
                st.session_state.job_preferences
            )
            st.session_state.job_matches = job_matches
    
    job_matches = st.session_state.job_matches
    
    if not job_matches:
        st.warning("No job matches found. Try adjusting your preferences.")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("← Back to Preferences", use_container_width=True):
                go_back()
                st.rerun()
    else:
        # Display a summary
        st.markdown(f"Found **{len(job_matches)}** job matches based on your resume and preferences.")
        
        # Filter options
        st.markdown("### Filter Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            min_match = st.slider("Minimum Match Score", 0, 100, 70, 5)
        
        with col2:
            location_filter = st.multiselect(
                "Location Type",
                options=["Remote", "Hybrid", "Onsite"],
                default=[]
            )
        
        with col3:
            # Extract unique companies
            companies = list(set(job["company"] for job in job_matches))
            company_filter = st.multiselect("Companies", options=companies, default=[])
        
        # Apply filters
        filtered_jobs = job_matches
        
        if min_match > 0:
            filtered_jobs = [job for job in filtered_jobs if job["match_score"] >= min_match]
        
        if location_filter:
            filtered_jobs = [
                job for job in filtered_jobs 
                if any(loc_type in job["location"] for loc_type in location_filter)
            ]
        
        if company_filter:
            filtered_jobs = [job for job in filtered_jobs if job["company"] in company_filter]
        
        # Display filtered matches
        st.markdown(f"### Showing {len(filtered_jobs)} of {len(job_matches)} matches")
        
        if not filtered_jobs:
            st.warning("No jobs match your current filters. Try adjusting the filter criteria.")
        
        # Display job cards
        for i, job in enumerate(filtered_jobs):
            with st.container():
                # Job card with customized styling
                st.markdown(f"""
                <div class="job-card">
                    <div class="job-header">
                        <div class="job-title-company">
                            <h3>{job['title']}</h3>
                            <h4>{job['company']}</h4>
                        </div>
                        <div class="match-score-container">
                            <div class="match-score match-{get_match_category(job['match_score'])}">
                                {job['match_score']}%
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
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
                    
                    with st.expander("Job Description"):
                        st.markdown(job["description"])
                
                with col2:
                    # Action buttons
                    apply_col, save_col = st.columns(2)
                    
                    with apply_col:
                        if st.button("Apply", key=f"apply_{i}"):
                            # Open application URL
                            st.markdown(f"<a href='{job['apply_url']}' target='_blank'>Apply Now</a>", unsafe_allow_html=True)
                    
                    with save_col:
                        saved_jobs = st.session_state.get("saved_jobs", [])
                        is_saved = any(saved_job["title"] == job["title"] and saved_job["company"] == job["company"] for saved_job in saved_jobs)
                        
                        if is_saved:
                            if st.button("Unsave", key=f"unsave_{i}"):
                                # Remove job from saved jobs
                                st.session_state.saved_jobs = [
                                    saved_job for saved_job in saved_jobs 
                                    if not (saved_job["title"] == job["title"] and saved_job["company"] == job["company"])
                                ]
                                st.rerun()
                        else:
                            if st.button("Save", key=f"save_{i}"):
                                # Add job to saved jobs
                                if "saved_jobs" not in st.session_state:
                                    st.session_state.saved_jobs = []
                                st.session_state.saved_jobs.append(job)
                                st.success(f"Saved: {job['title']} at {job['company']}")
                
                st.markdown("---")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("← Back to Preferences", use_container_width=True):
                go_back()
                st.rerun()
        
        with col3:
            if st.button("View Saved Jobs →", type="primary", use_container_width=True):
                advance_step()
                st.rerun()

def get_match_category(score):
    """Return a category based on match score for styling"""
    if score >= 90:
        return "excellent"
    elif score >= 80:
        return "great"
    elif score >= 70:
        return "good"
    else:
        return "fair"