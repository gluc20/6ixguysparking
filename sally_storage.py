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
                <path class="mane-outer" d="M200 20 L220 80 L180 80 Z" /><path class="mane-outer" d="M200 20 L240 70 L210 90 Z" /><path class="mane-outer" d="M200 20 L160 70 L190 90 Z" />
                <path class="mane-outer" d="M280 40 L300 100 L260 90 Z" /><path class="mane-outer" d="M320 80 L330 140 L290 120 Z" /><path class="mane-outer" d="M350 130 L340 190 L310 160 Z" />
                <path class="mane-outer" d="M360 190 L340 240 L320 200 Z" /><path class="mane-outer" d="M350 250 L320 290 L310 250 Z" />
                <path class="mane-outer" d="M120 40 L100 100 L140 90 Z" /><path class="mane-outer" d="M80 80 L70 140 L110 120 Z" /><path class="mane-outer" d="M50 130 L60 190 L90 160 Z" />
                <path class="mane-outer" d="M40 190 L60 240 L80 200 Z" /><path class="mane-outer" d="M50 250 L80 290 L90 250 Z" />
            </g>
            <g id="inner-mane">
                <path class="mane-inner" d="M200 60 L240 120 L200 140 L160 120 Z" /><path class="mane-inner" d="M260 90 L290 150 L240 160 L230 130 Z" />
                <path class="mane-inner" d="M300 140 L310 200 L260 190 L270 150 Z" /><path class="mane-inner" d="M310 210 L290 260 L250 240 L260 200 Z" />
                <path class="mane-inner" d="M140 90 L110 150 L160 160 L170 130 Z" /><path class="mane-inner" d="M100 140 L90 200 L140 190 L130 150 Z" /><path class="mane-inner" d="M90 210 L110 260 L150 240 L140 200 Z" />
            </g>
            <path class="face" d="M200 100 L240 140 L250 200 L240 260 L200 280 L160 260 L150 200 L160 140 Z" opacity="0.9"/>
            <path class="accent" d="M200 100 L220 140 L200 150 L180 140 Z" opacity="0.8"/>
            <g id="eyes">
                <path class="detail" d="M165 170 L185 165 L175 185 Z" /><path class="accent" d="M170 172 L182 168 L178 180 Z" />
                <path class="detail" d="M235 170 L215 165 L225 185 Z" /><path class="accent" d="M230 172 L218 168 L222 180 Z" />
            </g>
            <path class="detail" d="M200 200 L210 230 L190 230 Z" /><path class="accent" d="M200 205 L206 225 L194 225 Z" opacity="0.6"/>
            <path class="detail" d="M200 150 L200 200" opacity="0.5"/><path class="detail" d="M185 270 L200 285 L215 270" />
            <g opacity="0.3" stroke="white" stroke-width="1">
                <path d="M170 220 L150 215" /><path d="M170 225 L150 225" />
                <path d="M230 220 L250 215" /><path d="M230 225 L250 225" />
            </g>
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
