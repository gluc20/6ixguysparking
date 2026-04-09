import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="PRESTIGE ENTERPRISES", page_icon="🏢", layout="centered")

# 2. CSS Styling (Clean, Dark, Modern)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&display=swap');
    
    /* Background and Text */
    .stApp { background-color: #050505; color: #FFFFFF; }
    
    /* Elegant Header */
    .fancy-header {
        color: #FFFFFF; font-family: 'Playfair Display', serif;
        text-transform: uppercase; text-align: center;
        font-weight: 900; letter-spacing: 10px; font-size: 40px;
        border-bottom: 2px solid #FFFFFF; padding-bottom: 20px; width: 100%;
        margin-top: 10px; margin-bottom: 30px;
    }

    /* Logo Styling */
    .logo-container { text-align: center; padding: 20px 0; }
    .crest-outline { fill: none; stroke: #FFFFFF; stroke-width: 1.5; }
    .crest-fill { fill: #FFFFFF; }

    /* Forms and Chatbot UI */
    .stChatMessage { background-color: #0d0d0d !important; border: 1px solid #333; border-radius: 0px; }
    input, textarea { background-color: #0d0d0d !important; color: white !important; border: 1px solid #444 !important; border-radius: 0px !important; }
    .stButton>button { background-color: #FFFFFF !important; color: #000000 !important; font-weight: bold !important; width: 100%; border-radius: 0px; border: none; height: 50px; transition: 0.3s; }
    .stButton>button:hover { background-color: #cccccc !important; }

    /* Hide Streamlit Branding */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. Geometric Prestige "P" Crest (No Lion)
st.markdown("""
<div class='logo-container'>
    <svg width="150" height="150" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <path class="crest-outline" d="M50 5 L85 20 L85 55 C85 75 50 95 50 95 C50 95 15 75 15 55 L15 20 Z" />
        <path class="crest-fill" d="M40 30 H55 C62 30 65 33 65 38 C65 43 62 46 55 46 H45 V65 H40 V30 Z M45 35 V41 H54 C57 41 59 40 59 38 C59 36 57 35 54 35 H45 Z" />
    </svg>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='fancy-header'>PRESTIGE ENTERPRISES</div>", unsafe_allow_html=True)

# 4. Lead Capture Form
st.subheader("📩 Storage Inquiry")
st.write("Submit the form below for availability and current rates.")

with st.form("contact_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
    with col2:
        email = st.text_input("Email Address")
    
    msg = st.text_area("What are you looking to store? (RV, Boat, Containers, etc.)")
    
    submit_button = st.form_submit_button("SUBMIT TO GREG")

    if submit_button:
        if name and email and msg:
            # We use the standard endpoint to ensure maximum compatibility with Gmail
            form_data = {
                "name": name,
                "email": email,
                "message": msg,
                "_subject": f"New Prestige Inquiry from {name}"
            }
            try:
                response = requests.post("https://formsubmit.co/greguhl33@gmail.com", data=form_data)
                if response.status_code == 200:
                    st.success("✅ Inquiry Sent! Greg will review this and get back to you.")
                    st.info("Note: If this is your first time, check your email to confirm the FormSubmit activation.")
                else:
                    st.error("There was an issue sending your inquiry. Please try again.")
            except:
                st.error("Connection error. Please check your internet and try again.")
        else:
            st.warning("Please fill out all fields before submitting.")

st.divider()

# 5. Smart Chatbot
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you with your storage needs today?"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Automated Logic
    user_query = prompt.lower()
    if any(word in user_query for word in ["price", "cost", "rate", "how much"]):
        reply = "Our rates depend on the size of the vehicle or unit. Generally, RVs start at $150/mo and Boats at $120/mo. Please use the form above for a custom quote!"
    elif any(word in user_query for word in ["location", "where"]):
        reply = "We are located in the Niagara region. Submit an inquiry for the exact address and availability!"
    else:
        reply = "I'm here to help! For specific availability or to book a spot, please fill out the inquiry form above so Greg can contact you directly."

    with st.chat_message("assistant"):
        st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
