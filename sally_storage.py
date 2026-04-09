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
    
    .lion-svg { filter: drop-shadow(0 0 25px rgba(255,255,255,0.1)); }
</style>
""", unsafe_allow_html=True)

# --- HEADER WITH LEO MAGNUS ---
st.markdown("""
<div class='lion-container'>
    <svg class="lion-svg" width="320" height="320" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
        <path class="mane" d="M250 20 L270 100 L300 30 L285 105 L340 45 L320 115 L380 70 L350 125 L410 95 L370 140 L430 125 L385 160 L440 155 L390 185 L445 190 L395 210 L450 225 L400 235 L445 260 L395 265 L440 295 L390 295 L430 330 L380 325 L415 365 L365 355 L390 395 L345 380 L360 420 L320 400 L330 440 L295 415 L295 455 L265 425 L250 460 L235 425 L205 455 L205 415 L170 440 L180 400 L140 420 L155 380 L110 395 L135 355 L85 365 L120 325 L70 330 L110 295 L60 295 L105 265 L55 260 L100 240 L50 225 L105 210 L55 190 L110 185 L110 160 L115 125 L70 95 L150 70 L160 45 L170 115 L200 30 L215 105 L230 100 Z"/>
        <path class="mane-highlight" d="M250 60 L265 130 L295 75 L280 135 L330 85 L310 140 L360 105 L335 150 L385 130 L355 165 L400 155 L365 185 L405 185 L370 205 L410 220 L370 230 L405 255 L365 260 L395 290 L355 290 L380 325 L340 320 L360 360 L320 350 L335 385 L300 370 L305 405 L270 385 L265 420 L250 390 L235 420 L230 385 L195 405 L200 370 L165 385 L180 350 L140 360 L160 320 L120 325 L145 290 L105 290 L135 260 L95 255 L130 235 L90 220 L130 205 L95 185 L135 180 L135 155 L175 165 L195 105 L205 135 L220 75 L235 130 Z"/>
        <path class="face" d="M250 140 L290 165 L305 210 L300 260 L280 295 L250 310 L220 295 L200 260 L195 210 L210 165 Z"/>
        <path class="face" d="M250 140 L275 165 L250 175 L225 165 Z" fill="#e8e8e8"/>
        <path d="M225 195 L245 190 L240 208 L220 208 Z" fill="#1a1a1a" stroke="#ffffff" stroke-width="1"/>
        <path d="M275 195 L255 190 L260 208 L280 208 Z" fill="#1a1a1a" stroke="#ffffff" stroke-width="1"/>
        <path d="M228 198 L238 196 L236 203 L228 203 Z" class="eye"/>
        <path d="M272 198 L262 196 L264 203 L272 203 Z" class="eye"/>
        <path class="nose" d="M250 230 L270 260 L250 270 L230 260 Z"/>
        <path class="detail" d="M250 210 L250 230"/>
        <path class="face" d="M230 260 L220 285 L250 305 L280 285 L270 260 Z" fill="#c0c0c0"/>
        <path d="M235 275 L250 295 L265 275" fill="none" stroke="#333" stroke-width="2.5" stroke-linecap="round"/>
        <path class="detail" d="M225 270 L195 265 M225 275 L195 275 M225 280 L195 285" opacity="0.4"/>
        <path class="detail" d="M275 270 L305 265 M275 275 L305 275 M275 280 L305 285" opacity="0.4"/>
    </svg>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='fancy-header'>PRESTIGE ENTERPRISES</div>", unsafe_allow_html=True)

# --- LEAD CAPTURE ---
st.write("")
st.subheader("📩 Official Storage Inquiry")
with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email = st.text_input("Your Email")
    msg = st.text_area("Details (Vehicle, Size, etc.)")
    if st.form_submit_button("SUBMIT TO PRESTIGE ENTERPRISES"):
        if name and email and msg:
            res = requests.post("https://formsubmit.co/ajax/greguhl33@gmail.com", data={"name":name,"email":email,"message":msg})
            if res.status_code==200: st.success("Sent! Greg will contact you shortly.")
            else: st.error("Inquiry Error.")
        else: st.warning("Please fill all fields.")

st.divider()

# --- CHATBOT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to Prestige Enterprises. How can I help with your storage needs?"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

if p := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.write(p)
    info = {"rv":"$150/mo", "bus":"$200/mo", "boat":"$120/mo", "container":"$100/mo"}
    reply = "For specific availability and custom quotes, please use the form above!"
    for k, v in info.items():
        if k in p.lower(): reply = f"Our {k.upper()} storage starts at {v}. Please submit an inquiry for details!"
    with st.chat_message("assistant"): st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
