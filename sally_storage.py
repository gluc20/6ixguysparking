import streamlit as st
import smtplib
import sqlite3
import uuid
from datetime import datetime
from email.mime.text import MIMEText

# Mobile-first configuration
st.set_page_config(
    page_title="Prestige Storage",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Database init
DB_FILE = "prestige.db"
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inquiries 
                 (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, asset TEXT, 
                  size TEXT, months INTEGER, quote REAL, submitted TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (id INTEGER PRIMARY KEY, user_id TEXT, role TEXT, 
                  content TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# Phone numbers
PHONE_NUMBER = "6475216503"
WHATSAPP_NUMBER = "4374345822"
FORMATTED_PHONE = "(647) 521-6503"

# Mobile-First CSS
st.markdown("""
<style>
    .stApp {
        background: #0a0a0a;
        color: #fff;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        padding-bottom: 100px;
    }
    
    .mobile-header {
        text-align: center;
        padding: 20px 0 10px;
        border-bottom: 2px solid #333;
        margin-bottom: 20px;
    }
    .logo-text {
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -4px;
        color: #fff;
        line-height: 1;
        margin: 0;
    }
    .logo-text span {
        display: inline-block;
        transform: skewX(-12deg);
        border: 3px solid #fff;
        padding: 0 12px;
        margin: 0 2px;
    }
    .tagline {
        font-size: 12px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-top: 8px;
    }
    
    .stButton>button {
        background: #fff !important;
        color: #000 !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 8px !important;
        height: 56px !important;
        font-size: 16px !important;
        width: 100% !important;
        margin: 10px 0 !important;
        box-shadow: 0 4px 12px rgba(255,255,255,0.2) !important;
    }
    
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select,
    .stNumberInput>div>div>input,
    .stChatInput>div>div>input {
        background: #1a1a1a !important;
        color: #fff !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
        min-height: 48px !important;
        font-size: 16px !important;
        padding: 12px !important;
    }
    
    .streamlit-expanderHeader {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        color: #fff !important;
        font-size: 16px !important;
    }
    
    /* Chat styling for mobile */
    .stChatMessage {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        margin: 8px 0 !important;
        padding: 12px !important;
    }
    .stChatMessageContent {
        color: #fff !important;
    }
    
    /* Sticky bottom contact bar */
    .sticky-contact {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #fff;
        display: flex;
        justify-content: space-around;
        padding: 12px;
        z-index: 1000;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.5);
    }
    .sticky-btn {
        flex: 1;
        margin: 0 8px;
        text-align: center;
        padding: 14px;
        background: #000;
        color: #fff;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        font-size: 14px;
        border: none;
        cursor: pointer;
    }
    
    footer {display: none !important;}
    header {visibility: hidden;}
    
    .chat-container {
        background: #111;
        border-radius: 12px;
        padding: 15px;
        margin: 20px 0;
        border: 1px solid #333;
    }
    .chat-header {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)

# User ID for chat memory
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# Header
st.markdown("""
<div class="mobile-header">
    <div class="logo-text"><span>P</span><span>P</span></div>
    <div class="tagline">Prestige Storage Solutions</div>
</div>
""", unsafe_allow_html=True)

# Quick Value Prop
st.markdown("""
<p style="text-align: center; font-size: 18px; margin: 20px 0; color: #ddd;">
    Secure storage for RVs, Boats & Containers<br>
    <span style="color: #fff; font-weight: bold;">Ontario's Trusted Choice</span>
</p>
""", unsafe_allow_html=True)

# Essential Form
with st.form("quick_inquiry", clear_on_submit=True):
    st.markdown("### Get Your Quote")
    
    name = st.text_input("Your Name", placeholder="John Smith")
    phone = st.text_input("Phone Number", placeholder="(555) 123-4567")
    
    asset = st.selectbox("What are you storing?",
                        ["Select...", "RV / Motorhome", "Boat", "Shipping Container", 
                         "Commercial Truck", "Car / Trailer"],
                        index=0)
    
    size = st.select_slider("Size",
                           options=["Small", "Medium", "Large", "XL"],
                           value="Medium")
    
    months = st.number_input("How many months?", 
                            min_value=1, max_value=24, value=6)
    
    # Instant quote calculation
    if asset != "Select...":
        rates = {"Small": 70, "Medium": 95, "Large": 125, "XL": 160, "Container": 180}
        base = rates.get(size, 95)
        if months >= 12:
            base = int(base * 0.85)
        elif months >= 6:
            base = int(base * 0.90)
        
        total = base * months
        st.success(f"Estimated: ${base}/mo (${total} total)")
        st.session_state['calculated_quote'] = total
    else:
        st.session_state['calculated_quote'] = 0
    
    submitted = st.form_submit_button("GET MY QUOTE")
    
    if submitted:
        if name and phone and asset != "Select...":
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO inquiries (name, phone, asset, size, months, quote, submitted) VALUES (?,?,?,?,?,?,?)",
                     (name, phone, asset, size, months, 
                      st.session_state.get('calculated_quote', 0), 
                      datetime.now()))
            conn.commit()
            conn.close()
            
            # Send email
            try:
                sender = st.secrets.get("smtp_email", "your-email@gmail.com")
                pwd = st.secrets.get("smtp_password", "your-password")
                
                msg = MIMEText(f"New Inquiry:\nName: {name}\nPhone: {phone}\nAsset: {asset}\nSize: {size}\nMonths: {months}\nQuote: ${st.session_state.get('calculated_quote', 0)}")
                msg['Subject'] = f"New Lead: {name}"
                msg['From'] = sender
                msg['To'] = "greguhl33@gmail.com"
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender, pwd)
                server.send_message(msg)
                server.quit()
                
                st.balloons()
                st.success("Quote sent! Check your phone in 5 minutes.")
                
            except Exception as e:
                st.error("Email error, but your request is saved.")
        else:
            st.warning("Please fill in all fields")

# Pricing Accordion
with st.expander("View Full Pricing"):
    st.markdown("""
    **Small** (0-20ft): $60-80/mo  
    **Medium** (21-30ft): $80-110/mo  
    **Large** (31-40ft): $110-140/mo  
    **XL** (41-50ft): $140-180/mo  
    **Container**: $180-250/mo  
    
    *Winter storage (Oct-Apr): +25%*  
    *12-month prepay: 15% off*
    """)

# Trust Badges
st.markdown("""
<div style="display: flex; justify-content: space-around; margin: 30px 0; text-align: center; font-size: 12px; color: #666;">
    <div>24/7 Access<br>Available</div>
    <div>Gated &<br>Secure</div>
    <div>Instant<br>Quotes</div>
</div>
""", unsafe_allow_html=True)

# SALLY CHATBOT SECTION
st.markdown("---")
st.markdown("### Chat with Sally")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm Sally. Ask me about sizes, pricing, or availability!"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask Sally..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Simple Sally logic (no API needed for basic responses)
    prompt_lower = prompt.lower()
    
    if "price" in prompt_lower or "cost" in prompt_lower or "rate" in prompt_lower:
        response = "Our rates start at $60/month for small units and go up to $250 for large containers. Winter months (Oct-Apr) have a 25% premium. How big is your vehicle?"
    elif "size" in prompt_lower or "big" in prompt_lower or "fit" in prompt_lower:
        response = "We accommodate everything from compact cars to 50ft+ containers. Our spots are sized: Small (0-20ft), Medium (21-30ft), Large (31-40ft), and XL (40ft+). What are you storing?"
    elif "available" in prompt_lower or "spot" in prompt_lower or "now" in prompt_lower:
        response = f"We currently have spots open! Call me at {FORMATTED_PHONE} or WhatsApp {WHATSAPP_NUMBER} for immediate availability. I can hold a spot for 24 hours with a deposit."
    elif "electric" in prompt_lower or "power" in prompt_lower:
        response = "Yes! We offer electricity hookups for $35/month. Perfect for keeping RV batteries charged or boat systems maintained."
    elif "location" in prompt_lower or "where" in prompt_lower or "address" in prompt_lower:
        response = "We're located in Ontario with easy highway access. I'll text you the exact address and gate code once you submit the form above!"
    elif "hour" in prompt_lower or "access" in prompt_lower or "gate" in prompt_lower:
        response = "Standard access is 6AM-10PM daily. We offer 24/7 access upgrade for $17/month if you need late night entry."
    else:
        response = f"I'm here to help! For the fastest response, call me at {FORMATTED_PHONE} or WhatsApp {WHATSAPP_NUMBER}. You can also fill out the quote form above and I'll call you back within 10 minutes."
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)

# Spacer for bottom bar
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

# Sticky Bottom Contact Bar
st.markdown(f"""
<div class="sticky-contact">
    <a href="tel:+1{PHONE_NUMBER}" class="sticky-btn" style="background: #333;">
        CALL {FORMATTED_PHONE}
    </a>
    <a href="https://wa.me/1{WHATSAPP_NUMBER}?text=Hi%20Sally,%20I%20need%20a%20storage%20quote" 
       class="sticky-btn" style="background: #25D366;">
        WHATSAPP
    </a>
</div>
""", unsafe_allow_html=True)
