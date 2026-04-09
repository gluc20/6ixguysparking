import streamlit as st
import requests

st.set_page_config(page_title="PRESTIGE ENTERPRISES", page_icon="🦁", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&display=swap');

    /* Background and global text color to White */
    .stApp { background-color: #121212; color: #FFFFFF; }
    
    .fancy-header {
        color: #FFFFFF;
        font-family: 'Playfair Display', serif;
        text-transform: uppercase;
        text-align: center;
        font-weight: 900;
        letter-spacing: 8px;
        font-size: 50px;
        margin-top: 10px;
        border-bottom: 1px solid #FFFFFF;
        padding-bottom: 15px;
        display: inline-block;
        width: 100%;
    }
    
    .lion-container {
        text-align: center;
        padding-top: 20px;
    }

    h3, label, .stMarkdown p { color: #FFFFFF !important; }

    .stChatMessage { background-color: #1e1e1e !important; color: white !important; border: 1px solid #444; }
    
    input, textarea { 
        background-color: #1e1e1e !important; 
        color: white !important; 
        border: 1px solid #FFFFFF !important; 
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .stButton>button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 2px !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("""
    <div class='lion-container'>
        <svg width="100" height="100" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 3L10 7L6 8L8 11L7 15L12 13L17 15L16 11L18 8L14 7L12 3Z" fill="white"/>
            <path d="M12 13V17M10 18H14" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M5 10C3 12 3 15 5 18M19 10C21 12 21 15 19 18" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)

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

# --- CHATBOT ---
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
        st.
