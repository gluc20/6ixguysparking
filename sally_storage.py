import streamlit as st
import requests

st.set_page_config(page_title="PRESTIGE ENTERPRISES", page_icon="🦁", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&display=swap');

    .stApp { background-color: #121212; color: white; }
    
    .fancy-header {
        color: #D4AF37;
        font-family: 'Playfair Display', serif;
        text-transform: uppercase;
        text-align: center;
        font-weight: 900;
        letter-spacing: 5px;
        font-size: 55px;
        margin-top: -20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5), 0 0 15px rgba(212, 175, 55, 0.3);
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 10px;
        display: inline-block;
        width: 100%;
    }
    
    .lion-icon {
        text-align: center;
        font-size: 80px;
        margin-bottom: 0px;
    }

    .stChatMessage { background-color: #1e1e1e !important; color: white !important; border: 1px solid #333; }
    input, textarea { background-color: #1e1e1e !important; color: white !important; border: 1px solid #D4AF37 !important; }
    #MainMenu, footer, header {visibility: hidden;}
    
    .stButton>button {
        background-color: #D4AF37 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 5px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("<div class='lion-icon'>🦁</div>", unsafe_allow_html=True)
st.markdown("<div class='fancy-header'>PRESTIGE ENTERPRISES</div>", unsafe_allow_html=True)
st.write("") 

# --- LEAD CAPTURE FORM ---
st.subheader("📩 Official Storage Inquiry")
with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    c_email = st.text_input("Your Email Address")
    details = st.text_area("What are you looking to store? (Vehicle type, size, etc.)")
    submitted = st.form_submit_button("SUBMIT TO PRESTIGE ENTERPRISES")

    if submitted:
        if name and c_email and details:
            url = "https://formsubmit.co/ajax/greguhl33@gmail.com"
            payload = {"name": name, "email": c_email, "message": details, "_subject": f"PRESTIGE Lead: {name}"}
            res = requests.post(url, data=payload)
            if res.status_code == 200:
                st.success("Inquiry sent. Greg will contact you shortly.")
            else:
                st.error("Error. Please try again.")
        else:
            st.warning("Please fill in all fields.")

st.divider()

# --- CHATBOT WITH AUTO-GREETING ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Thank you for choosing Prestige Enterprises. How can we assist you with your storage needs today?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask a quick question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    storage_info = {"rv": "RV: $150/mo", "bus": "Bus: $200/mo", "boat": "Boat: $120/mo", "container": "Container: $100/mo"}
    ans = "For detailed pricing or custom quotes, please use the Official Inquiry form above so Greg can contact you directly!"
    
    for key in storage_info:
        if key in prompt.lower():
            price = storage_info[key].split(': ')[1]
            ans = f
