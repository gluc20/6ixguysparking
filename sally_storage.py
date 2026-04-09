import streamlit as st
import requests

st.set_page_config(page_title="PRESTIGE ENTERPRISES", page_icon="🦁", layout="centered")

# --- CSS STYLE & ANIMATIONS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&display=swap');
    .stApp { background-color: #050505; color: #FFFFFF; }
    .fancy-header {
        color: #FFFFFF; font-family: 'Playfair Display', serif;
        text-transform: uppercase; text-align: center;
        font-weight: 900; letter-spacing: 8px; font-size: 42px;
        border-bottom: 1px solid #FFFFFF; padding-bottom: 15px; width: 100%;
        margin-top: 10px;
    }
    .lion-container { text-align: center; padding-top: 10px; }
    .stChatMessage { background-color: #0a0a0a !important; border: 1px solid #333; }
    input, textarea { background-color: #0a0a0a !important; color: white !important; border: 1px solid #FFFFFF !important; }
    .stButton>button { background-color: #FFFFFF !important; color: #000000 !important; font-weight: bold !important; width: 100%; border-radius: 0px; }
    #MainMenu, footer, header {visibility: hidden;}

    /* LEO MAGNUS SVG STYLING */
    .mane { fill: #0a0a0a; stroke: #e5e5e5; stroke-width: 2.5; stroke-linejoin: round; }
    .mane-highlight { fill: #1a1a1a; stroke: #ffffff; stroke-width: 1.5; }
    .face { fill: #d4d4d4; stroke: #ffffff; stroke-width: 2; }
    .eye { fill: #ffffff; }
    .nose { fill: #2a2a2a; stroke: #ffffff; stroke-width: 2; }
    .detail { stroke: #666; stroke-width: 1.5; fill: none; opacity: 0.6; }
    
    .lion-svg { filter: drop-shadow(0 0 25px rgba(255,255,255,0.1)); transition: 0.5s; }
    .lion-svg:hover { filter: drop-shadow(0 0 35px rgba(255,255,255,0.25)); }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER WITH LEO MAGNUS ---
st.markdown("""
    <div class='lion-container'>
        <svg class="lion-svg" width="320" height="320" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
            <path class="mane" d="M250 20 L270 100 L300 30 L285 105 L340 45 L320 115 L380 70 L350 125 L410 95 L370 140 L430 125 L385 160 L440 15
