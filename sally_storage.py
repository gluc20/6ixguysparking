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
    
    /* Geometric SVG Classes */
    .mane-outer { fill: #1a1a1a; stroke: #ffffff; stroke-width: 2.5; stroke-linejoin: round; }
    .mane-inner { fill: #2a2a2a; stroke: #cccccc; stroke-width: 1.5; stroke-linejoin: round; }
    .face-base { fill: #d4d4d4; stroke: #ffffff; stroke-width: 2; }
    .face-highlight { fill: #ffffff; }
    .eye-socket { fill: #1a1a1a; }
    .eye { fill: #ffffff; }
    .nose { fill: #333333; }
    .detail-line { stroke: #666666; stroke-width: 1; fill: none; }
    .accent { fill: #ffffff; opacity: 0.9; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER WITH THE MASTERPIECE LION ---
st.markdown("""
    <div class='lion-container'>
        <svg width="280" height="280" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
            <circle cx="200" cy="200" r="195" fill="#0a0a0a" stroke="#333" stroke-width="1"/>
            <g id="mane">
                <path class="mane-outer" d="M200 20 L210 70 L230 30 L220 75 L250 45 L235 80 L270 70 L245 90 L290 95 L255 105 L300 125 L260 115 L295 150 L255 130 L275 170 L240 145 L255 190 L220 160 L225 200 L200 165 L175 200 L180 160 L145 190 L160 145 L125 170 L145 130 L105 150 L140 115 L100 125 L145 105 L110 95 L155 90 L130 70 L165 80 L150 45 L180 75 L170 30 L190 70 Z" />
                <path class="mane-inner" d="M200 50 L215 90 L235 55 L225 95 L260 75 L240 100 L280 95 L250 115 L290 135 L255 125 L275 155 L240 135 L250 175 L220 145 L220 185 L200 150 L180 185 L180 145 L150 175 L160 135 L125 155 L145 125 L110 135 L150 115 L120 95 L160 100 L140 75 L175 95 L165 55 L185 90 Z" />
            </g>
            <path class="face-base" d="M200 80 L240 130 L250 200 L235 270 L200 300 L165 270 L150 200 L160 130 Z" />
            <path class="face-highlight" d="M200 80 L220 125 L200 135 L180 125 Z" opacity="0.6"/>
            <path class="accent" d="M200 85 L215 120 L200 128 L185 120 Z" />
            <path class="eye-socket" d="M170 160 L185 155 L182 175 L168 178 Z" />
            <path class="eye-socket" d="M230 160 L215 155 L218 175 L232 178 Z" />
            <path class="eye" d="M172 165 L183 162 L180 172 L173 173 Z" />
            <path class="eye" d="M228 165 L217 162 L220 172 L227 173 Z" />
            <circle cx="178" cy="167" r="1.5" fill="#000"/>
            <circle cx="222" cy="167" r="1.5" fill="#000"/>
            <path class="nose" d="M200 185 L210 215 L190 215 Z" />
            <path class="accent" d="M200 190 L205 210 L195 210 Z" opacity="0.4"/>
            <path class="detail-line" d="M200 135 L200 185" />
            <path class="detail-line" d="M190 140 L195 175" opacity="0.5"/>
            <path class="detail-line" d="M210 140 L205 175" opacity="0.5"/>
            <path class="detail-line" d="M190 215 L200 245 L210 215" stroke-width="2"/>
            <path class="detail-line" d="M200 245 L200 265" stroke-width="2"/>
            <path class="detail-line" d="M185 215 L180 240 L195 255 L200 265 L205 255 L220 240 L215 215" opacity="0.6"/>
            <path class="accent" d="M190 260 L200 275 L210 260 Z" opacity="0.3"/>
            <g opacity="0.2" stroke="white" stroke-width="1">
                <path d="M180 230 L160 225" /><path d="M182 235 L162 235" /><path d="M185 240 L165 245" />
                <path d="M220 230 L240 225" /><path d="M218 235 L238 235" /><path d="M215 240 L235 245" />
            </g>
            <path class="mane-outer" d="M140 100 L130 70 L155 90 Z" />
            <path class="mane-outer" d="M260 100 L270 70 L245 90 Z" />
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
    st.session_state.messages = [{"role": "assistant", "content": "Hello! Thank you for choosing Prestige Enterprises. How can we assist you today?"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

if p := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.write(p)
    info = {"rv":"$150/mo", "bus":"$200/mo", "boat":"$120/mo", "container":"$100/mo"}
    reply = "For custom quotes, please use the form above!"
    for k, v in info.items():
        if k in p.lower(): reply = f"Our {k.upper()} storage starts at {v}. Use the form above to book!"
    with st.chat_message("assistant"): st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
