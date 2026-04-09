import streamlit as st
import requests

st.set_page_config(page_title="6ixGuysParking G Enterprises", page_icon="🦁", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    h1 { color: #D4AF37 !important; font-family: 'Garamond', serif; text-transform: uppercase; text-align: center; font-weight: 900; }
    .sub { color: #ffffff; text-align: center; font-weight: bold; text-transform: uppercase; font-size: 0.8rem; }
    .stChatMessage { background-color: #1e1e1e !important; color: white !important; border: 1px solid #333; }
    input, textarea { background-color: #1e1e1e !important; color: white !important; border: 1px solid #D4AF37 !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='font-size: 80px;'>🦁</h1><h1>6ixGuysParking</h1><p class='sub'>G Enterprises</p>", unsafe_allow_html=True)
st.divider()

# --- LEAD CAPTURE FORM ---
st.subheader("📩 Official Storage Inquiry")
with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    c_email = st.text_input("Your Email Address")
    details = st.text_area("What are you looking to store? (Vehicle type, size, etc.)")
    submitted = st.form_submit_button("Submit to G Enterprises")

    if submitted:
        if name and c_email and details:
            url = "https://formsubmit.co/ajax/greguhl33@gmail.com"
            payload = {"name": name, "email": c_email, "message": details, "_subject": f"GParking Lead: {name}"}
            res = requests.post(url, data=payload)
            if res.status_code == 200:
                st.success("Inquiry sent. Greg will contact you shortly.")
            else:
                st.error("Error. Please try again.")
        else:
            st.warning("Please fill in all fields.")

st.divider()

# --- CHATBOT WITH AUTO-GREETING ---
# This section tells the bot to say hello first!
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Thank you for choosing Prestige Enterprises. How can we assist you with your storage needs today?"}
    ]

# This part "draws" the conversation on the screen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# This part handles new questions
if prompt := st.chat_input("Ask a quick question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    storage_info = {"rv": "RV: $150/mo", "bus": "Bus: $200/mo", "boat": "Boat: $120/mo", "container": "Container: $100/mo"}
    ans = "For detailed pricing or custom quotes, please use the Official Inquiry form above so Greg can contact you directly!"
    
    for key in storage_info:
        if key in prompt.lower():
            ans = f"Our storage for {key.upper()} starts at {storage_info[key].split(': ')[1]}. Fill out the form above to secure your spot!"
    
    with st.chat_message("assistant"):
        st.write(ans)
    st.session_state.messages.append({"role": "assistant", "content": ans})
    
