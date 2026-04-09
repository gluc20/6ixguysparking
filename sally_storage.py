import streamlit as st
st.set_page_config(page_title="6ixGuysParking G Enterprises", page_icon="🦁", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    h1 { color: #D4AF37 !important; font-family: "Garamond", serif; text-transform: uppercase; text-align: center; font-weight: 900; }
    .sub { color: #ffffff; text-align: center; font-weight: bold; text-transform: uppercase; font-size: 0.8rem; }
    .stChatMessage { background-color: #1e1e1e !important; color: white !important; border: 1px solid #333; }
    .stMarkdown p { color: #ffffff !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
st.markdown("<h1 style=\"font-size: 80px;\">🦁</h1><h1>6ixGuysParking</h1><p class=\"sub\">G Enterprises</p>", unsafe_allow_html=True)
st.divider()
storage_info = {"rv": "RV: $150/mo", "bus": "Bus: $200/mo", "boat": "Boat: $120/mo", "container": "Container: $100/mo"}
def get_response(user_input):
    user_input = user_input.lower()
    for key in storage_info:
        if key in user_input: return storage_info[key]
    return "Welcome to 6ixGuysParking G Enterprises. How can we help?"
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])
if prompt := st.chat_input("Inquire here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)
    ans = get_response(prompt)
    with st.chat_message("assistant"): st.write(ans)
    st.session_state.messages.append({"role": "assistant", "content": ans})