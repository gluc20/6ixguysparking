import streamlit as st
import requests

st.set_page_config(page_title="PRESTIGE ENTERPRISES", page_icon="🦁", layout="centered")

# --- CSS STYLE & ANIMATIONS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&display=swap');
    .stApp { background-color: #000000; color: #FFFFFF; }
    .fancy-header {
        color: #FFFFFF; font-family: 'Playfair Display', serif;
        text-transform: uppercase; text-align: center;
        font-weight: 900; letter-spacing: 8px; font-size: 42px;
        border-bottom: 1px solid #FFFFFF; padding-bottom: 15px; width: 100%;
        margin-top: 10px;
    }
    .lion-container { text-align: center; padding-top: 10px; position: relative; }
    .stChatMessage { background-color: #0d0d0d !important; border: 1px solid #333; }
    input, textarea { background-color: #0d0d0d !important; color: white !important; border: 1px solid #FFFFFF !important; }
    .stButton>button { background-color: #FFFFFF !important; color: #000000 !important; font-weight: bold !important; width: 100%; border-radius: 0px; }
    #MainMenu, footer, header {visibility: hidden;}

    /* LION LOGO STYLING */
    .mane-outer { fill: #0d0d0d; stroke: #ffffff; stroke-width: 2.5; stroke-linejoin: round; }
    .mane-mid { fill: #1a1a1a; stroke: #c0c0c0; stroke-width: 1.8; stroke-linejoin: round; }
    .mane-inner { fill: #262626; stroke: #808080; stroke-width: 1.2; stroke-linejoin: round; }
    .face-skin { fill: #d4d4d4; stroke: #ffffff; stroke-width: 2; }
    .bone-structure { fill: none; stroke: #ffffff; stroke-width: 1.5; }
    .eye-socket { fill: #0a0a0a; stroke: #404040; stroke-width: 1; }
    .eye-glow { fill: #ffffff; }
    .nose-prism { fill: #1a1a1a; stroke: #ffffff; stroke-width: 2; }
    .brow-ridge { fill: #d4d4d4; stroke: #ffffff; stroke-width: 1.5; }

    @keyframes breathe {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(255,255,255,0.1)); }
        50% { filter: drop-shadow(0 0 40px rgba(255,255,255,0.25)); }
    }
    .breathing-lion { animation: breathe 4s ease-in-out infinite; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER WITH ULTIMATE LION ---
st.markdown("""
    <div class='lion-container'>
        <svg class="breathing-lion" width="300" height="300" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
            <circle cx="200" cy="200" r="190" fill="#000000" stroke="#222" stroke-width="1"/>
            <path class="mane-outer" d="M200 15 L210 75 L230 25 L225 80 L260 35 L250 85 L290 50 L275 95 L315 70 L295 105 L340 95 L315 125 L355 120 L325 140 L365 150 L330 160 L360 180 L325 175 L350 205 L315 190 L335 225 L300 205 L310 245 L280 220 L285 260 L255 230 L255 270 L230 240 L225 280 L205 250 L195 285 L180 250 L160 280 L165 240 L140 270 L145 230 L120 260 L125 220 L95 245 L105 205 L70 225 L90 190 L55 205 L80 175 L45 180 L75 160 L35 150 L75 140 L45 120 L85 125 L60 95 L105 105 L85 70 L125 95 L110 50 L150 85 L140 35 L175 80 L170 25 L190 75 Z" />
            <path class="mane-mid" d="M200 55 L215 105 L240 65 L230 110 L270 80 L250 120 L290 110 L265 135 L300 150 L265 145 L285 175 L255 160 L265 195 L235 175 L240 210 L215 185 L215 225 L195 195 L195 225 L175 195 L170 225 L165 185 L140 210 L145 175 L115 195 L125 160 L95 175 L115 145 L80 150 L115 135 L90 110 L130 120 L120 80 L155 110 L145 65 L175 105 Z" />
            <path class="mane-inner" d="M200 85 L210 120 L230 95 L220 125 L250 110 L235 135 L265 130 L240 150 L265 155 L240 165 L255 185 L230 170 L235 200 L215 175 L215 205 L200 180 L185 205 L185 175 L165 200 L170 170 L145 185 L160 165 L135 155 L160 150 L135 130 L165 135 L150 110 L180 125 L170 95 L190 120 Z" />
            <path class="face-skin" d="M200 100 L245 145 L255 205 L240 265 L200 295 L160 265 L145 205 L155 145 Z" />
            <path class="brow-ridge" d="M200 100 L220 140 L200 150 L180 140 Z" />
            <path class="eye-socket" d="M170 170 L188 165 L185 188 L165 190 Z" />
            <path class="eye-socket" d="M230 170 L212 165 L215 188 L235 190 Z" />
            <path class="eye-glow" d="M172 175 L183 172 L180 182 L173 183 Z" />
            <path class="eye-glow" d="M228 175 L217 172 L220 182 L227 183 Z" />
            <circle cx="177" cy="177" r="2" fill="#000"/>
            <circle cx="223" cy="177" r="2" fill="#000"/>
            <path class="bone-structure" d="M200 150 L200 195" />
            <path class="nose-prism" d="M200 195 L218 225 L200 235 L182 225 Z" />
            <path class="bone-structure" d="M182 225 L190 245 L200 255 L210 245 L218 225" stroke-width="2"/>
            <path class="bone-structure" d="M195 275 L200 285 L205 275" stroke-width="2" />
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
        if k in p.lower(): reply = f"Our {k.upper()} storage options start at {v}. Please submit an inquiry for details!"
    with st.chat_message("assistant"): st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
