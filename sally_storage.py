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
    .lion-container { text-align: center; padding-top: 20px; }
    .stChatMessage { background-color: #1e1e1e !important; color: white !important; border: 1px solid #444; }
    input, textarea { background-color: #1e1e1e !important; color: white !important; border: 1px solid #FFFFFF !important; }
    .stButton>button { background-color: #FFFFFF !important; color: #000000 !important; font-weight: bold !important; width: 100%; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<div class='lion-container'><svg width='100' height='100' viewBox='0 0 24 24' fill='none'><path d='M12 3L10 7L6 8L8 11L7 15L12 13L17 15L16 11L18 8L14 7L12 3Z' fill='white'/><path d='M12 13V17M10 18H14' stroke='white' stroke-width='1.5'/><path d='M5 10C3 12 3 15 5 18M19 10C21 12 21 15 19 18' stroke='white' stroke-width='1.5'/></svg></div>", unsafe_allow_html=True)
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
            st.success("Sent! Greg will contact you shortly.") if res.status_code==200 else st.error("Error sending.")
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
