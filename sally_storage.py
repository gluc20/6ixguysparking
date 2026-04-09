import streamlit as st
import requests

st.set_page_config(page_title="PRESTIGE ENTERPRISES", page_icon="🦁", layout="centered")

# --- CSS STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&display=swap');
    .stApp { background-color: #0a0a0a; color: #FFFFFF; }
    .fancy-header {
        color: #FFFFFF; font-family: 'Playfair Display', serif;
        text-transform: uppercase; text-align: center;
        font-weight: 900; letter-spacing: 8px; font-size: 42px;
        border-bottom: 1px solid #FFFFFF; padding-bottom: 15px; width: 100%;
        margin-top: 10px;
    }
    .lion-container { text-align: center; padding-top: 10px; }
    .stChatMessage { background-color: #1a1a1a !important; border: 1px solid #333; }
    input, textarea { background-color: #1a1a1a !important; color: white !important; border: 1px solid #FFFFFF !important; }
    .stButton>button { background-color: #FFFFFF !important; color: #000000 !important; font-weight: bold !important; width: 100%; border-radius: 0px; }
    #MainMenu, footer, header {visibility: hidden;}
    
    .mane-outer { fill: #2a2a2a; stroke: #ffffff; stroke-width: 2; }
    .mane-inner { fill: #1a1a1a; stroke: #cccccc; stroke-width: 1.5; }
    .face { fill: #e0e0e0; }
    .accent { fill: #ffffff; }
    .detail { stroke: #ffffff; stroke-width: 1.5; fill: none; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER WITH GEOMETRIC LION ---
st.markdown("""
    <div class='lion-container'>
        <svg width="250" height="250" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
            <circle cx="200" cy="200" r="190" fill="#000000" stroke="#333333" stroke-width="2"/>
            <g id="outer-mane">
                <path class="mane-outer" d="M200 20 L220 80 L180 80 Z" />
                <path class="mane-outer" d="M200 20 L240 70 L210 90 Z" />
                <path class="mane-outer" d="M200 20 L160 70 L190 90 Z" />
                <path class="mane-outer" d="M280 40 L300 100 L260 90 Z" />
                <path class="mane-outer" d="M320 80 L330 140 L290 120 Z" />
                <path class="mane-outer" d="M350 130 L340 190 L310 160 Z" />
                <path class="mane-outer" d="M360 190 L340 240 L320 200 Z" />
                <path class="mane-outer" d="M350 250 L320 290 L310 250 Z" />
                <path class="mane-outer" d="M120 40 L100 100 L140 90 Z" />
                <path class="mane-outer" d="M80 80 L70 140 L110 120 Z" />
                <path class="mane-outer" d="M50 130 L60 190 L90 160 Z" />
                <path class="mane-outer" d="M40 190 L60 240 L80 200 Z" />
                <path class="mane-outer" d
