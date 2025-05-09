import streamlit as st

def colored_header(label, description=None, color_name="blue-70"):
    """
    Shows a header with a colored underline and an optional description.
    """
    colors = {
        "blue-70": "#1E3A8A",
        "blue-30": "#3B82F6",
        "green-70": "#0D9488",
        "green-30": "#14B8A6",
        "orange-70": "#EA580C",
        "orange-30": "#F59E0B",
        "red-70": "#B91C1C",
        "red-30": "#EF4444",
        "violet-70": "#6D28D9",
        "violet-30": "#8B5CF6",
    }
    
    if color_name not in colors:
        color_name = "blue-70"
        
    color = colors[color_name]
    
    st.markdown(
        f"""
        <div style="background-color:{color};padding:0.5px;border-radius:3px;">
        </div>
        <h2 style="color:{color};margin-top:10px;">{label}</h2>
        """,
        unsafe_allow_html=True,
    )
    
    if description:
        st.caption(f"{description}")