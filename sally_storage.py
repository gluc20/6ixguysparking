import streamlit as st
import requests

st.set_page_config(page_title="PRESTIGE ENTERPRISES", page_icon="🦁", layout="centered")

# --- CSS STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&display=swap');
    .stApp { background-color: #121212; color: #FFFFFF; }
    .fancy-header {
        color: #FFFFFF; font-family: 'Playfair Display', serif;
        text-transform: uppercase; text-align: center;
        font-weight: 900; letter-spacing: 8px; font-size: 50px;
        border-bottom: 1px solid #FFFFFF; padding-bottom: 15px; width: 100%;
    }
    .lion-container { text-align: center; padding-top: 20px; padding-bottom: 10px; }
    .stChatMessage { background-color: #1e1e1e !important; color: white !important; border: 1px solid #444; }
    input, textarea { background-color: #1e1e1e !important; color: white !important; border: 1px solid #FFFFFF !important; }
    .stButton>button { background-color: #FFFFFF !important; color: #000000 !important; font-weight: bold !important; width: 100%; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER WITH ACTUAL LION HEAD ---
st.markdown("""
    <div class='lion-container'>
        <svg width="120" height="120" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C10 2 8 3 7 5C5 4 3 5 2 7C2 9 3 10 4 11C3 12 2 14 2 16C2 19 5 22 12 22C19 22 22 19 22 16C22 14 21 12 20 11C21 10 22 9 22 7C21 5 19 4 17 5C16 3 14 2 12 2Z" stroke="white" stroke-width="1.5"/>
            <path d="M9 10C9 10 10 9 12 9C14 9 15 10 15 10" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M10 13H14L12 16L10 13Z" fill="white"/>
            <path d="M8 12C8 12 7 13 7 15C7 17 9 18 12 18C15 18 17 17 17 15C17 13 16 12 16 12" stroke="white" stroke-width="1.5"/>
            <path d="M12 16V18" stroke="white" stroke-width="1.5"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='fancy-header'>PRESTIGE ENTERPRISES</div>", unsafe_allow_html=True)

# --- FORM ---
st.subheader("📩 Official Storage Inquiry")
with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email = st.text_input("Your Email")
    msg = st.text_area("Details (Vehicle, Size, etc.)")
    if st.form_submit_button("SUBMIT TO PRESTIGE ENTERPRISES"):
        if name and email and msg:
            res = requests.post("https://formsubmit.co/ajax/greguhl33@gmail.com", data={"name":name,"email":email,"message":msg})
            if res.status_code==200: st.success("Sent! Greg will contact you shortly.")
            else: st.error("Error sending.")
        else: st.warning("Fill in all fields.")

st.divider()

# --- CHAT ---
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
