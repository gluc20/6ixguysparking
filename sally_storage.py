import streamlit as st
import requests

st.set_page_config(page_title="PRESTIGE ENTERPRISES", page_icon="🦁", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&display=swap');

    /* Background and global text color to White */
    .stApp { background-color: #121212; color: #FFFFFF; }
    
    .fancy-header {
        color: #FFFFFF;
        font-family: 'Playfair Display', serif;
        text-transform: uppercase;
        text-align: center;
        font-weight: 900;
        letter-spacing: 8px;
        font-size: 50px;
        margin-top: 10px;
        border-bottom: 1px solid #FFFFFF;
        padding-bottom: 15px;
        display: inline-block;
        width: 100%;
    }
    
    .lion-container {
        text-align: center;
        padding-top: 20px;
    }

    /* Subheader and Form Labels to White */
    h3, label, .stMarkdown p { color: #FFFFFF !important; }

    .stChatMessage { background-color: #1e1e1e !important; color: white !important; border: 1px solid #444; }
    
    /* Form Inputs */
    input, textarea { 
        background-color: #1e1e1e !important; 
        color: white !important; 
        border: 1px solid #FFFFFF !important; 
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Button Style - Modern White/Black */
    .stButton>button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 2px !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
# Using a high-quality SVG/Icon style for a Modern Majesty White Lion
st.markdown("""
    <div class='lion-container'>
        <svg width="100" height="100" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C10.5 2 9 3 8 4.5C7 3.5 5.5 3 4 3C2 3 1 4.5 1 6.5C1 10.5 5 14 12 21C19 14 23 10.5 23 6.5C23 4.5 22 3 20 3C18.5 3 17 3.5 16 4.5
