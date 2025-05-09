import streamlit as st
import random
from typing import Dict, List, Any
import openai
import os
import json

def match_jobs_with_ai(resume_data: Dict[str, Any], preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Match resume data with jobs using OpenAI
    """
    api_key = "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"
    
    # If no API key is available, use mock data
    if not api_key:
        st.warning("No OpenAI API key found. Using mock data for demonstration.")
        return generate_mock_job_matches(resume_data, preferences)
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # Create a prompt that includes the resume data and preferences
        skills_str = ", ".join(resume_data.get("skills", []))
        experience_str = "\n".join([
            f"- {exp['title']} at {exp['company']} ({exp['dates']}): {exp['description']}"
            for exp in resume_data.get("experience", [])
        ])
        education_str = "\n".join([
            f"- {edu['degree']} from {edu['institution']} ({edu['dates']})"
            for edu in resume_data.get("education", [])
        ])
        
        prompt = f"""
        Based on the following resume information and job preferences, generate 5 relevant job matches.
        
        Resume Information:
        Skills: {skills_str}
        
        Experience:
        {experience_str}
        
        Education:
        {education_str}
        
        Job Preferences:
        - Location Type: {preferences.get('location_type', 'Any')}
        - Experience Level: {preferences.get('experience_level', 'Any')}
        - Job Type: {preferences.get('job_type', 'Full-time')}
        - Industry: {preferences.get('industry', 'Any')}
        
        For each job match, provide:
        1. Job title
        2. Company name
        3. Location (including whether it's remote, hybrid, or onsite)
        4. Salary range
        5. Required skills (ordered by importance)
        6. Job description
        7. A matching score from 0-100 based on how well the resume matches the job
        8. Application URL
        
        Format your response as a JSON array of job objects.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a job matching expert. Your task is to generate highly relevant job matches based on resume data and preferences."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        content = response.choices[0].message.content
        jobs_data = json.loads(content)
        
        # Ensure we have a list of jobs
        if isinstance(jobs_data, dict) and "jobs" in jobs_data:
            jobs = jobs_data["jobs"]
        elif isinstance(jobs_data, list):
            jobs = jobs_data
        else:
            jobs = []
            
        return jobs
    
    except Exception as e:
        st.error(f"Error matching jobs with AI: {e}")
        return generate_mock_job_matches(resume_data, preferences)

def generate_mock_job_matches(resume_data: Dict[str, Any], preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate mock job match data"""
    from faker import Faker
    fake = Faker()
    
    # Use resume skills to make matches somewhat relevant
    skills = resume_data.get("skills", ["Python", "Data Analysis", "Project Management"])
    
    # Job titles related to common skills
    job_titles = [
        "Senior Software Engineer", 
        "Data Scientist",
        "Product Manager",
        "Full Stack Developer",
        "UX/UI Designer",
        "DevOps Engineer",
        "AI Researcher",
        "Machine Learning Engineer"
    ]
    
    # Location preferences
    location_type = preferences.get("location_type", "Any")
    if location_type == "Remote":
        locations = ["Remote", "Remote", "Remote", "Remote (US)", "Remote (Global)"]
    elif location_type == "Hybrid":
        locations = ["Hybrid - New York, NY", "Hybrid - San Francisco, CA", "Hybrid - Austin, TX", 
                   "Hybrid - Seattle, WA", "Hybrid - Boston, MA"]
    elif location_type == "Onsite":
        locations = ["New York, NY", "San Francisco, CA", "Austin, TX", "Seattle, WA", "Boston, MA"]
    else:
        locations = ["Remote", "Hybrid - New York, NY", "San Francisco, CA", 
                   "Remote (US)", "Hybrid - Austin, TX"]
    
    # Generate 5-8 job matches
    num_matches = random.randint(5, 8)
    job_matches = []
    
    for i in range(num_matches):
        # Select some of the resume skills plus some additional ones
        user_skills = set(skills)
        all_skills = list(user_skills) + ["Teamwork", "Communication", "Problem Solving", 
                                       "Java", "JavaScript", "React", "Node.js", "AWS",
                                       "Docker", "Kubernetes", "SQL", "NoSQL", "Git",
                                       "CI/CD", "Agile", "Scrum"]
        
        # Randomly select 5-10 required skills, prioritizing those from the resume
        num_required = random.randint(5, 10)
        resume_skills_count = min(len(user_skills), num_required - 2)
        required_skills = list(random.sample(list(user_skills), resume_skills_count))
        
        # Add some additional skills
        remaining_skills = [s for s in all_skills if s not in required_skills]
        required_skills.extend(random.sample(remaining_skills, num_required - len(required_skills)))
        
        # Calculate match score based on how many of the user's skills match
        skill_match_pct = len(set(skills).intersection(set(required_skills))) / len(required_skills)
        match_score = int(70 + skill_match_pct * 30) 
        
        # Randomize match score a bit to add variety
        match_score = min(100, max(70, match_score + random.randint(-5, 5)))
        
        # Salary ranges based on job title seniority hints
        title = random.choice(job_titles)
        if "Senior" in title or "Lead" in title:
            salary_range = f"${random.randint(120, 180)}K - ${random.randint(181, 220)}K"
        else:
            salary_range = f"${random.randint(80, 110)}K - ${random.randint(111, 150)}K"
        
        job_match = {
            "title": title,
            "company": fake.company(),
            "location": random.choice(locations),
            "salary": salary_range,
            "required_skills": required_skills,
            "description": fake.paragraph(nb_sentences=random.randint(4, 7)),
            "match_score": match_score,
            "apply_url": f"https://example.com/jobs/{i+1}"
        }
        
        job_matches.append(job_match)
    
    # Sort by match score descending
    job_matches.sort(key=lambda x: x["match_score"], reverse=True)
    return job_matches