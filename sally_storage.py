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
        font-weight: 900; letter-spacing: 8px; font-size: 45px;
        border-bottom: 1px solid #FFFFFF; padding-bottom: 15px; width: 100%;
    }
    .lion-container { text-align: center; padding-top: 30px; padding-bottom: 10px; }
    .stChatMessage { background-color: #1e1e1e !important; border: 1px solid #444; }
    input, textarea { background-color: #1e1e1e !important; color: white !important; border: 1px solid #FFFFFF !important; }
    .stButton>button { background-color: #FFFFFF !important; color: #000000 !important; font-weight: bold !important; width: 100%; border-radius: 0px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER WITH MAJESTIC LION ---
st.markdown("""
    <div class='lion-container'>
        <svg width="150" height="150" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C10 2 8.5 3 7 4C5 3 3 4 2 6C1 8 1 10 2 12C1 13 1 15 2 17C3 19 5 21 8 22C10 22.5 14 22.5 16 22C19 21 21 19 22 17C23 15 23 13 22 12C23 10 23 8 22 6C21 4 19 3 17 4C15.5 3 14 2 12 2Z" fill="white"/>
            <path d="M12 7L10 11L8 12L10 13L9 16L12 15L15 16L14 13L16 12L14 11L12 7Z" fill="#121212"/>
            <path d="M11 18H13M12 15V18" stroke="#121212" stroke-width="0.8"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='fancy-header'>PRESTIGE ENTERPRISES</div>", unsafe_allow_html=True)

# --- FORM ---
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
