import streamlit as st
import smtplib
import sqlite3
import json
import uuid
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Mobile-first configuration
st.set_page_config(
    page_title="Prestige Storage",
    page_icon="",
    layout="centered",  # Single column for mobile
    initial_sidebar_state="collapsed"
)

# Database init (lightweight)
DB_FILE = "prestige.db"
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inquiries 
                 (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, asset TEXT, 
                  size TEXT, months INTEGER, quote REAL, submitted TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# Mobile-First CSS (Large touch targets, thumb-friendly)
st.markdown("""
<style>
    /* Reset for mobile */
    .stApp {
        background: #0a0a0a;
        color: #fff;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Mobile header - compact */
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
    
    /* Huge touch targets for mobile */
    .stButton>button {
        background: #fff !important;
        color: #000 !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 8px !important;
        height: 56px !important;  /* Large thumb target */
        font-size: 16px !important;
        width: 100% !important;
        margin: 10px 0 !important;
        box-shadow: 0 4px 12px rgba(255,255,255,0.2) !important;
    }
    
    /* Large inputs for mobile typing */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select,
    .stNumberInput>div>div>input {
        background: #1a1a1a !important;
        color: #fff !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
        min-height: 48px !important;  /* Easy to tap */
        font-size: 16px !important;   /* Prevent zoom on iOS */
        padding: 12px !important;
    }
    
    /* Accordion for compact pricing */
    .streamlit-expanderHeader {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        color: #fff !important;
        font-size: 16px !important;
    }
    
    /* Sticky bottom contact bar (mobile classic pattern) */
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
        padding: 12px;
        background: #000;
        color: #fff;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        font-size: 14px;
    }
    
    /* Hide Streamlit footer for clean mobile look */
    footer {display: none !important;}
    header {visibility: hidden;}
    
    /* Quick-select chips for mobile */
    .asset-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 15px 0;
    }
    .chip {
        background: #1a1a1a;
        border: 2px solid #444;
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 14px;
        cursor: pointer;
        text-align: center;
        flex: 1;
        min-width: 80px;
    }
    .chip:hover {
        border-color: #fff;
        background: #333;
    }
    
    /* WhatsApp floating button (FAB) */
    .whatsapp-fab {
        position: fixed;
        bottom: 80px;
        right: 20px;
        background: #25D366;
        color: white;
        width: 56px;
        height: 56px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 999;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# Mobile Header (Compact)
st.markdown("""
<div class="mobile-header">
    <div class="logo-text"><span>P</span><span>P</span></div>
    <div class="tagline">Premium Outdoor Storage</div>
</div>
""", unsafe_allow_html=True)

# Quick Value Prop (Mobile users scan fast)
st.markdown("""
<p style="text-align: center; font-size: 18px; margin: 20px 0; color: #ddd;">
    Secure storage for RVs, Boats & Containers<br>
    <span style="color: #fff; font-weight: bold;">Ontario's Trusted Choice</span>
</p>
""", unsafe_allow_html=True)

# Essential Form Only (Mobile optimized - no sidebar)
with st.form("quick_inquiry", clear_on_submit=True):
    st.markdown("### Get Your Quote")
    
    # Large, easy-tap inputs
    name = st.text_input("Your Name", placeholder="John Smith", 
                        help="Required")
    
    phone = st.text_input("Phone Number", placeholder="(555) 123-4567",
                         help="We'll text you the quote")
    
    # Asset selection - Large buttons via selectbox
    asset = st.selectbox("What are you storing?",
                        ["Select...", "RV / Motorhome", "Boat", "Shipping Container", 
                         "Commercial Truck", "Car / Trailer"],
                        index=0)
    
    # Size - Simplified for mobile
    size = st.select_slider("Size",
                           options=["Small", "Medium", "Large", "XL"],
                           value="Medium",
                           help="Small: under 20ft, Medium: 21-30ft, etc.")
    
    # Duration with visual indicator
    months = st.number_input("How many months?", 
                            min_value=1, max_value=24, value=6,
                            help="Longer = better rates")
    
    # Instant quote calculation (no AI needed - fast)
    if asset != "Select...":
        rates = {"Small": 70, "Medium": 95, "Large": 125, "XL": 160, "Container": 180}
        base = rates.get(size, 95)
        if months >= 12:
            base = int(base * 0.85)
        elif months >= 6:
            base = int(base * 0.90)
        
        total = base * months
        st.success(f"Estimated: ${base}/mo (${total} total)")
        
        # Save for email
        st.session_state['calculated_quote'] = total
    else:
        st.session_state['calculated_quote'] = 0
    
    # Big submit button
    submitted = st.form_submit_button("GET MY QUOTE")
    
    if submitted:
        if name and phone and asset != "Select...":
            # Fast DB insert
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO inquiries (name, phone, asset, size, months, quote, submitted) VALUES (?,?,?,?,?,?,?)",
                     (name, phone, asset, size, months, 
                      st.session_state.get('calculated_quote', 0), 
                      datetime.now()))
            conn.commit()
            conn.close()
            
            # Send email (async would be better, but sync for reliability)
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

# Collapsible Pricing (Saves screen space)
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

# Trust Badges (Mobile friendly)
st.markdown("""
<div style="display: flex; justify-content: space-around; margin: 30px 0; text-align: center; font-size: 12px; color: #666;">
    <div>24/7 Access<br>Available</div>
    <div>Gated &<br>Secure</div>
    <div>Instant<br>Quotes</div>
</div>
""", unsafe_allow_html=True)

# Sticky Bottom Contact Bar (Mobile UX Pattern)
st.markdown("""
<div class="sticky-contact">
    <a href="tel:555-123-4567" class="sticky-btn" style="background: #333;">CALL NOW</a>
    <a href="https://wa.me/15551234567?text=I%20need%20a%20storage%20quote" class="sticky-btn" style="background: #25D366;">WHATSAPP</a>
</div>
""", unsafe_allow_html=True)

# Spacer for bottom bar
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
