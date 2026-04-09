import streamlit as st
import requests

st.set_page_config(page_title="PRESTIGE ENTERPRISES", page_icon="📦", layout="centered")

# --- CSS STYLE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&display=swap');
    .stApp { background-color: #050505; color: #FFFFFF; }
    .fancy-header {
        color: #FFFFFF; font-family: 'Playfair Display', serif;
        text-transform: uppercase; text-align: center;
        font-weight: 900; letter-spacing: 8px; font-size: 42px;
        border-bottom: 1px solid #FFFFFF; padding-bottom: 15px; width: 100%;
        margin-top: 20px;
    }
    .logo-container { text-align: center; padding-top: 30px; }
    .stChatMessage { background-color: #0a0a0a !important; border: 1px solid #333; }
    input, textarea { background-color: #0a0a0a !important; color: white !important; border: 1px solid #FFFFFF !important; }
    .stButton>button { background-color: #FFFFFF !important; color: #000000 !important; font-weight: bold !important; width: 100%; border-radius: 0px; }
    #MainMenu, footer, header {visibility: hidden;}

    /* GEOMETRIC VAULT LOGO */
    .vault-main { fill: none; stroke: #FFFFFF; stroke-width: 2; stroke-linejoin: bevel; }
    .vault-accent { fill: #FFFFFF; opacity: 0.1; }
    .vault-line { stroke: #FFFFFF; stroke-width: 1; opacity: 0.5; }
</style>
""", unsafe_allow_html=True)

# --- HEADER WITH GEOMETRIC VAULT LOGO ---
st.markdown("""
<div class='logo-container'>
    <svg width="200" height="200" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <path class="vault-main" d="M50 5 L90 25 L90 75 L50 95 L10 75 L10 25 Z" />
        <path class="vault-main" d="M50 15 L80 35 L80 65 L50 85 L20 65 L20 35 Z" />
        <line class="vault-line" x1="50" y1="5" x2="50" y2="95" />
        <line class="vault-line" x1="10" y1="25" x2="90" y2="75" />
        <line class="vault-line" x1="90" y1="25" x2="10" y2="75" />
        <circle cx="50" cy="50" r="8" class="vault-main" />
        <path d="M50 42 L58 50 L50 58 L42 50 Z" fill="#FFFFFF" />
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
    if st.form_submit_button("SUBMIT INQUIRY"):
        if name and email and msg:
            res = requests.post("https://formsubmit.co/ajax/greguhl33@gmail.com", data={"name":name,"email":email,"message":msg})
            if res.status_code==200: st.success("Inquiry Received. We will contact you shortly.")
            else: st.error("Submission Error.")
        else: st.warning("Please fill all fields.")

st.divider()

# --- CHATBOT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to Prestige Enterprises. How can I assist you with your storage needs?"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

if p := st.chat_input("Ask about rates or availability..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.write(p)
    
    # Simple Logic
    reply = "For specific availability and custom quotes, please use the form above!"
    if "rv" in p.lower(): reply = "RV storage starts at $150/mo. Submit the form for a spot!"
    elif "boat" in p.lower(): reply = "Boat storage starts at $120/mo. Use the form above to check availability."
    
    with st.chat_message("assistant"): st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
