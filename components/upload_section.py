import streamlit as st
import json
from utils.resume_parser import extract_text_from_pdf, parse_resume_with_ai
from utils.session_state import advance_step

def render_upload_section():
    """Render the resume upload section"""
    st.markdown("## Upload Your Resume")
    st.markdown("Upload your resume to start the matching process. We support PDF and text files.")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"], key="resume_uploader")
    
    # Process uploaded file
    if uploaded_file is not None:
        with st.spinner("Processing your resume..."):
            # Extract text based on file type
            if uploaded_file.name.endswith('.pdf'):
                resume_text = extract_text_from_pdf(uploaded_file)
            else:  # .txt file
                resume_text = uploaded_file.getvalue().decode("utf-8")
            
            # Store the raw text in session state
            st.session_state.resume_text = resume_text
            
            # Parse the resume text
            if resume_text:
                resume_data = parse_resume_with_ai(resume_text)
                st.session_state.resume_data = resume_data
                
                # Display parsed information
                display_parsed_resume(resume_data)
                
                # Continue button
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Continue to Job Preferences", type="primary", use_container_width=True):
                        advance_step()
                        st.rerun()
            else:
                st.error("Could not extract text from the uploaded file. Please try another file.")
    
    # Sample resume option
    st.markdown("---")
    if st.button("Use Sample Resume", key="sample_resume"):
        with st.spinner("Loading sample resume..."):
            # Load sample resume data
            sample_data = {
                "name": "Alex Johnson",
                "contact": {"email": "alex.johnson@example.com", "phone": "555-123-4567"},
                "skills": ["Python", "Data Analysis", "Machine Learning", "SQL", "React", 
                           "Project Management", "Communication", "Team Leadership"],
                "experience": [
                    {
                        "company": "TechCorp Solutions",
                        "title": "Senior Data Scientist",
                        "dates": "2020-2023",
                        "description": "Led a team of data scientists in developing predictive models that increased customer retention by 25%."
                    },
                    {
                        "company": "DataViz Inc.",
                        "title": "Data Analyst",
                        "dates": "2017-2020",
                        "description": "Developed dashboards and reports that helped optimize marketing campaigns, resulting in a 15% increase in ROI."
                    }
                ],
                "education": [
                    {
                        "institution": "Stanford University",
                        "degree": "M.S. in Computer Science",
                        "dates": "2015-2017"
                    },
                    {
                        "institution": "University of California, Berkeley",
                        "degree": "B.S. in Statistics",
                        "dates": "2011-2015"
                    }
                ],
                "certifications": ["AWS Certified Data Analytics", "Google Professional Data Engineer"],
                "languages": ["English", "Mandarin"]
            }
            
            # Store the sample data
            st.session_state.resume_data = sample_data
            st.session_state.resume_text = "Sample resume text"
            
            # Display parsed information
            display_parsed_resume(sample_data)
            
            # Continue button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Continue to Job Preferences", type="primary", key="continue_sample", use_container_width=True):
                    advance_step()
                    st.rerun()

def display_parsed_resume(resume_data):
    """Display the parsed resume information"""
    st.markdown("### Parsed Resume Information")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Name:** {resume_data.get('name', 'Not found')}")
        st.markdown(f"**Email:** {resume_data.get('contact', {}).get('email', 'Not found')}")
        st.markdown(f"**Phone:** {resume_data.get('contact', {}).get('phone', 'Not found')}")
        
        st.markdown("#### Skills")
        skills = resume_data.get("skills", [])
        if skills:
            for skill in skills:
                st.markdown(f"- {skill}")
        else:
            st.markdown("No skills found")
            
        st.markdown("#### Education")
        education = resume_data.get("education", [])
        if education:
            for edu in education:
                st.markdown(f"- {edu.get('degree')} from {edu.get('institution')} ({edu.get('dates')})")
        else:
            st.markdown("No education information found")
    
    with col2:
        st.markdown("#### Experience")
        experience = resume_data.get("experience", [])
        if experience:
            for exp in experience:
                with st.expander(f"{exp.get('title')} at {exp.get('company')}"):
                    st.markdown(f"**Dates:** {exp.get('dates')}")
                    st.markdown(f"**Description:** {exp.get('description')}")
        else:
            st.markdown("No experience information found")
            
        if resume_data.get("certifications"):
            st.markdown("#### Certifications")
            for cert in resume_data.get("certifications", []):
                st.markdown(f"- {cert}")
                
        if resume_data.get("languages"):
            st.markdown("#### Languages")
            for lang in resume_data.get("languages", []):
                st.markdown(f"- {lang}")
    
    # Edit option
    with st.expander("Edit Parsed Information"):
        st.markdown("""
        You can edit the parsed information below. This will help improve your job matches.
        """)
        
        # Convert the resume data to JSON string with indentation for better readability
        resume_json = json.dumps(resume_data, indent=2)
        edited_json = st.text_area("Edit Resume Data (JSON format)", value=resume_json, height=300)
        
        if st.button("Update Resume Data"):
            try:
                # Parse the edited JSON string back to dictionary
                updated_resume_data = json.loads(edited_json)
                st.session_state.resume_data = updated_resume_data
                st.success("Resume data updated successfully!")
                st.rerun()
            except json.JSONDecodeError:
                st.error("Invalid JSON format. Please check your edits.")