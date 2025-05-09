import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the app"""
    
    custom_css = """
    <style>
        /* Main Colors */
        :root {
            --primary-color: #001F3F; /* Navy Blue */
            --primary-light: #3B82F6;
            --accent-color: #0D9488;
            --highlight-color: #F59E0B;
            --bg-color: #001F3F; /* Changed background color to Navy Blue */
            --text-color: #1E293B;
            --light-gray: #E2E8F0;
            --dark-gray: #64748B;
            --success-color: #10B981;
            --warning-color: #F59E0B;
            --error-color: #EF4444;
        }
        
        /* Typography */
        .main-header h1 {
            font-size: 3.5rem;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 0;
            letter-spacing: -0.025em;
        }
        
        .main-header .accent {
            color: var(--accent-color);
        }
        
        .main-header .subtitle {
            font-size: 1.2rem;
            color: var(--dark-gray);
            margin-top: 0;
            margin-bottom: 2rem;
        }
        
        /* Steps Indicator */
        .step {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
            opacity: 0.6;
            transition: all 0.3s ease;
        }
        
        .step.current {
            opacity: 1;
        }
        
        .step.completed {
            opacity: 0.8;
        }
        
        .step-number {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background-color: var(--light-gray);
            color: var(--dark-gray);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 10px;
        }
        
        .step.current .step-number {
            background-color: var(--primary-color);
            color: white;
        }
        
        .step.completed .step-number {
            background-color: var(--accent-color);
            color: white;
        }
        
        .step-text {
            font-weight: 500;
        }
        
        /* Divider */
        .divider {
            margin-top: 1rem;
            margin-bottom: 2rem;
            border: none;
            height: 1px;
            background-color: var(--light-gray);
        }
        
        /* Job Cards */
        .job-card {
            padding: 10px 0;
            transition: all 0.2s ease;
        }
        
        .job-card:hover {
            transform: translateY(-2px);
        }
        
        .job-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }
        
        .job-title-company h3 {
            margin: 0;
            color: var(--primary-color);
            font-size: 1.3rem;
        }
        
        .job-title-company h4 {
            margin: 5px 0 10px 0;
            color: var(--dark-gray);
            font-size: 1rem;
        }
        
        .match-score-container {
            display: flex;
            align-items: center;
        }
        
        .match-score {
            padding: 4px 10px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .match-excellent {
            background-color: #DCFCE7;
            color: #166534;
        }
        
        .match-great {
            background-color: #E0F2FE;
            color: #0C4A6E;
        }
        
        .match-good {
            background-color: #FEF3C7;
            color: #92400E;
        }
        
        .match-fair {
            background-color: #FEE2E2;
            color: #991B1B;
        }
        
        /* Skills Pills */
        .skills-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 10px 0;
        }
        
        .skill {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            background-color: var(--light-gray);
            color: var(--dark-gray);
        }
        
        .skill.match {
            background-color: var(--primary-light);
            color: white;
        }
        
        /* Buttons */
        .stButton button {
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        
        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        /* File uploader */
        .uploadedFile {
            border-radius: 10px;
            border: 1px dashed var(--accent-color);
            padding: 10px;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stMarkdown, .stButton, .stSelectbox, .stMultiselect, .stRadio, .stSlider, .stTextInput, .stNumberInput {
            animation: fadeIn 0.5s ease-out;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #f8fafc;
            border-right: 1px solid var(--light-gray);
        }
        
        [data-testid="stSidebar"] .sidebar-content {
            padding: 1rem;
        }
        
        /* Expander customization */
        .streamlit-expanderHeader {
            font-weight: 600;
            color: var(--primary-color);
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2.5rem;
            }
            
            .job-header {
                flex-direction: column;
            }
            
            .match-score-container {
                margin-top: 10px;
            }
        }
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)