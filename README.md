# CVibe - Resume Analyzer & Job Matcher

CVibe is an AI-powered application that helps job seekers match their resumes with suitable job vacancies. The application parses resumes, extracts relevant skills and experience, and then matches them with job opportunities based on user preferences.

## Features

- **Resume Upload**: Support for PDF and text resume formats
- **AI Resume Parsing**: Extract skills, experience, education, and other relevant information
- **Customizable Job Preferences**: Set location type (remote, hybrid, onsite), experience level, job type, and industry preferences
- **Intelligent Job Matching**: Match your resume with job opportunities based on your skills and preferences
- **Job Management**: Save interesting job opportunities and track your applications

## Installation

1. Clone the repository
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables (optional)
   - Create a `.env` file in the root directory
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

## Usage

Run the application:

```
streamlit run app.py
```

The application will be available at `http://localhost:8501`.

## Project Structure

```
CVibe/
├── app.py                      # Main application file
├── components/                 # UI components
│   ├── about.py               # About section with saved jobs
│   ├── job_matches.py         # Job matching results display
│   ├── job_preferences.py     # Job preference selection
│   ├── sidebar.py             # Application sidebar
│   └── upload_section.py      # Resume upload interface
├── styles/
│   └── custom_styles.py       # Custom CSS styles
├── utils/
│   ├── job_matcher.py         # Job matching logic
│   ├── resume_parser.py       # Resume parsing utilities
│   └── session_state.py       # Session state management
├── streamlit_extras/          # Custom Streamlit components
│   └── colored_header.py      # Colored header component
└── requirements.txt           # Project dependencies
```

## Deployment

This application is designed to be deployed on Streamlit Community Cloud. Follow these steps to deploy:

1. Push your code to GitHub
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/)
3. Create a new app, select your repository, branch, and specify `app.py` as the main file
4. If needed, add your OpenAI API key in the app secrets

## Dependencies

- streamlit
- pandas
- pdfplumber
- python-dotenv
- openai
- faker (for demo data)

## License

MIT

## Authors

Your Name