import streamlit as st
import pdfplumber
import re
import os
from typing import Dict, List, Any, Tuple
import openai

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from a PDF file"""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

def parse_resume_with_ai(resume_text: str) -> Dict[str, Any]:
    """
    Parse resume text using OpenAI to extract structured information
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    # If no API key is available, use mock data
    if not api_key:
        st.warning("No OpenAI API key found. Using mock data for demonstration.")
        return generate_mock_resume_data(resume_text)
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        system_prompt = """
        You are an expert resume parser. Extract the following information from the resume:
        1. Full name
        2. Contact information (email, phone)
        3. Skills (technical and soft skills)
        4. Work experience (company names, job titles, dates, and descriptions)
        5. Education (institutions, degrees, dates)
        6. Certifications
        7. Languages
        
        Format your response as JSON with the following structure:
        {
            "name": "...",
            "contact": {"email": "...", "phone": "..."},
            "skills": ["skill1", "skill2", ...],
            "experience": [
                {"company": "...", "title": "...", "dates": "...", "description": "..."},
                ...
            ],
            "education": [
                {"institution": "...", "degree": "...", "dates": "..."},
                ...
            ],
            "certifications": ["cert1", "cert2", ...],
            "languages": ["language1", "language2", ...]
        }
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": resume_text}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        parsed_data = eval(response.choices[0].message.content)
        return parsed_data
    
    except Exception as e:
        st.error(f"Error parsing resume with AI: {e}")
        return generate_mock_resume_data(resume_text)

def extract_skills_keywords(text: str) -> List[str]:
    """Extract potential skills from text using regex patterns"""
    # This is a simple keyword extraction, AI-based extraction would be more robust
    common_skills = [
        "python", "java", "javascript", "html", "css", "react", "angular", "vue", 
        "node.js", "express", "django", "flask", "sql", "nosql", "mongodb", 
        "postgresql", "mysql", "aws", "azure", "gcp", "docker", "kubernetes",
        "ci/cd", "git", "agile", "scrum", "communication", "leadership", 
        "problem solving", "critical thinking", "teamwork", "project management"
    ]
    
    found_skills = []
    for skill in common_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.append(skill)
    
    return found_skills

def generate_mock_resume_data(resume_text: str) -> Dict[str, Any]:
    """Generate mock parsed resume data when OpenAI API is not available"""
    from faker import Faker
    fake = Faker()
    
    # Extract some basic info from the text to make it somewhat relevant
    skills = extract_skills_keywords(resume_text)
    if not skills:
        skills = ["Python", "Data Analysis", "Project Management", "Communication"]
    
    return {
        "name": fake.name(),
        "contact": {
            "email": fake.email(),
            "phone": fake.phone_number()
        },
        "skills": skills,
        "experience": [
            {
                "company": fake.company(),
                "title": "Senior Developer",
                "dates": "2019-2023",
                "description": "Led a team of developers in building enterprise applications."
            },
            {
                "company": fake.company(),
                "title": "Software Engineer",
                "dates": "2016-2019",
                "description": "Developed and maintained web applications using React and Node.js."
            }
        ],
        "education": [
            {
                "institution": fake.university(),
                "degree": "Master's in Computer Science",
                "dates": "2014-2016"
            },
            {
                "institution": fake.university(),
                "degree": "Bachelor's in Information Technology",
                "dates": "2010-2014"
            }
        ],
        "certifications": ["AWS Certified Developer", "Scrum Master"],
        "languages": ["English", "Spanish"]
    }