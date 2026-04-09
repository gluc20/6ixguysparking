import streamlit as st
import smtplib
import sqlite3
import uuid
import base64
from datetime import datetime
from email.mime.text import MIMEText

# ========== FREE PWA CONFIGURATION ==========
# This makes your website work like a native app when added to home screen

PWA_MANIFEST = {
    "name": "Prestige Storage",
    "short_name": "Prestige",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0a0a0a",
    "theme_color": "#0a0a0a",
    "orientation": "portrait",
    "icons": [
        {
            "src": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxOTIgMTkyIj48cmVjdCB3aWR0aD0iMTkyIiBoZWlnaHQ9IjE5MiIgZmlsbD0iIzBhMGEwYSIgcng9IjI0Ii8+PHRleHQgeD0iOTYiIHk9IjEyNSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjgwIiBmb250LXdlaWdodD0iYm9sZCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPjx0c3BhbiBzdHlsZT0iZm9udC1zdHlsZTogaXRhbGljIj5QPC90c3Bhbj48dHNwYW4gc3R5bGU9ImZvbnQtc3R5bGU6IGl0YWxpYyI+UDwvdHNwYW4+PC90ZXh0Pjwvc3ZnPg==",
            "sizes": "192x192",
            "type": "image/svg+xml"
        },
        {
            "src": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48cmVjdCB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgZmlsbD0iIzBhMGEwYSIgcng9IjQ4Ii8+PHRleHQgeD0iMjU2IiB5PSIzNDAiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIyMDAiIGZvbnQtd2VpZ2h0PSJib2xkIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+PHRzcGFuIHN0eWxlPSJmb250LXN0eWxlOiBpdGFsaWMiPlA8L3RzcGFuPjx0c3BhbiBzdHlsZT0iZm9udC1zdHlsZTogaXRhbGljIj5QPC90c3Bhbj48L3RleHQ+PC9zdmc+",
            "sizes": "512x512",
            "type": "image/svg+xml"
        }
    ]
}

manifest_json = str(PWA_MANIFEST).replace("'", '"')
manifest_b64 = base64.b64encode(manifest_json.encode()).decode()

# ========== STREAMLIT PAGE CONFIG ==========
st.set_page_config(
    page_title="Prestige Storage",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========== PWA META TAGS & SERVICE WORKER ==========
st.markdown(f"""
    <link rel="manifest" href="data:application/json;base64,{manifest_b64}">
    <meta name="theme-color" content="#0a0a0a">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Prestige Storage">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <!-- iOS Icons -->
    <link rel="apple-touch-icon" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxOTIgMTkyIj48cmVjdCB3aWR0aD0iMTkyIiBoZWlnaHQ9IjE5MiIgZmlsbD0iIzBhMGEwYSIgcng9IjI0Ii8+PHRleHQgeD0iOTYiIHk9IjEyNSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjgwIiBmb250LXdlaWdodD0iYm9sZCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPjx0c3BhbiBzdHlsZT0iZm9udC1zdHlsZTogaXRhbGljIj5QPC90c3Bhbj48dHNwYW4gc3R5bGU9ImZvbnQtc3R5bGU6IGl0YWxpYyI+UDwvdHNwYW4+PC90ZXh0Pjwvc3ZnPg==">
    <link rel="apple-touch-icon" sizes="152x152" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNTIgMTUyIj48cmVjdCB3aWR0aD0iMTUyIiBoZWlnaHQ9IjE1MiIgZmlsbD0iIzBhMGEwYSIgcng9IjI0Ii8+PHRleHQgeD0iNzYiIHk9IjEwMCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjYwIiBmb250LXdlaWdodD0iYm9sZCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPjx0c3BhbiBzdHlsZT0iZm9udC1zdHlsZTogaXRhbGljIj5QPC90c3Bhbj48dHNwYW4gc3R5bGU9ImZvbnQtc3R5bGU6IGl0YWxpYyI+UDwvdHNwYW4+PC90ZXh0Pjwvc3ZnPg==">
    <link rel="apple-touch-icon" sizes="180x180" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxODAgMTgwIj48cmVjdCB3aWR0aD0iMTgwIiBoZWlnaHQ9IjE4MCIgZmlsbD0iIzBhMGEwYSIgcng9IjI0Ii8+PHRleHQgeD0iOTAiIHk9IjEyMCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjcwIiBmb250LXdlaWdodD0iYm9sZCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPjx0c3BhbiBzdHlsZT0iZm9udC1zdHlsZTogaXRhbGljIj5QPC90c3Bhbj48dHNwYW4gc3R5bGU9ImZvbnQtc3R5bGU6IGl0YWxpYyI+UDwvdHNwYW4+PC90ZXh0Pjwvc3ZnPg==">
    
    <style>
        /* PWA Install Banner */
        .pwa-banner {{
            position: fixed;
            bottom: 90px;
            left: 10px;
            right: 10px;
            background: #1a1a1a;
            border: 2px solid #fff;
            color: white;
            padding: 15px;
            border-radius: 12px;
            z-index: 10000;
            display: none;
            text-align: center;
            font-family: -apple-system, sans-serif;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }}
        .pwa-banner.show {{ display: block; }}
        .pwa-banner-btn {{
            background: white;
            color: black;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            margin-top: 10px;
            font-weight: bold;
            cursor: pointer;
            display: inline-block;
            margin-right: 10px;
        }}
        .pwa-banner-close {{
            background: none;
            border: none;
            color: #888;
            cursor: pointer;
            font-size: 18px;
        }}
        
        /* Hide Streamlit elements in standalone mode for app-like feel */
        @media all and (display-mode: standalone) {{
            #MainMenu {{visibility: hidden !important;}}
            footer {{visibility: hidden !important;}}
            header {{visibility: hidden !important;}}
            .stDeployButton {{display: none !important;}}
            .stActionButton {{display: none !important;}}
        }}
        
        /* iOS safe area padding */
        body {{
            padding-top: env(safe-area-inset-top, 0);
            padding-bottom: env(safe-area-inset-bottom, 0);
        }}
    </style>
    
    <div id="pwa-install-banner" class="pwa-banner">
        <strong>Install Prestige Storage</strong><br>
        Add to your home screen for instant access<br>
        <button class="pwa-banner-btn" onclick="installPWA()">Install Now</button>
        <button class="pwa-banner-close" onclick="document.getElementById('pwa-install-banner').style.display='none'">×</button>
    </div>
    
    <script>
        // Service Worker for offline functionality
        if ('serviceWorker' in navigator) {{
            const swCode = `
                self.addEventListener('install', e => {{
                    self.skipWaiting();
                }});
                self.addEventListener('fetch', e => {{
                    e.respondWith(
                        fetch(e.request).catch(() => {{
                            return new Response('Offline mode - using cached data');
                        }})
                    );
                }});
            `;
            const swBlob = new Blob([swCode], {{type: 'application/javascript'}});
            const swUrl = URL.createObjectURL(swBlob);
            navigator.serviceWorker.register(swUrl).catch(() => {{}});
        }}
        
        // Detect iOS Safari
        const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
        const isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
        
        let deferredPrompt;
        
        // Android install prompt
        window.addEventListener('beforeinstallprompt', (e) => {{
            e.preventDefault();
            deferredPrompt = e;
            if (!isStandalone) {{
                document.getElementById('pwa-install-banner').classList.add('show');
            }}
        }});
        
        // iOS detection (no native prompt, show manual instructions)
        if (isIOS && !isStandalone && !deferredPrompt) {{
            setTimeout(() => {{
                document.getElementById('pwa-install-banner').classList.add('show');
            }}, 2000);
        }}
        
        function installPWA() {{
            if (deferredPrompt) {{
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {{
                    if (choiceResult.outcome === 'accepted') {{
                        console.log('PWA installed');
                    }}
                    deferredPrompt = null;
                    document.getElementById('pwa-install-banner').style.display = 'none';
                }});
            }} else if (isIOS) {{
                alert('To install: tap the Share button (box with arrow) at the bottom of Safari, then scroll down and tap "Add to Home Screen"');
            }}
        }}
    </script>
""", unsafe_allow_html=True)

# ========== DATABASE SETUP ==========
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

# ========== CONTACT INFO ==========
PHONE_NUMBER = "6475216503"
WHATSAPP_NUMBER = "4374345822"
FORMATTED_PHONE = "(647) 521-6503"

# ========== MOBILE CSS ==========
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
    
    .sticky-contact {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #fff;
        display: flex;
        justify-content: space-around;
        padding: 12px;
        z-index: 9999;
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
</style>
""", unsafe_allow_html=True)

# ========== USER SESSION ==========
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# ========== HEADER ==========
st.markdown("""
<div class="mobile-header">
    <div class="logo-text"><span>P</span><span>P</span></div>
    <div class="tagline">Prestige Storage Solutions</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="text-align: center; font-size: 18px; margin: 20px 0; color: #ddd;">
    Secure storage for RVs, Boats, Trucks & Trailers<br>
    <span style="color: #fff; font-weight: bold;">Ontario's Trusted Choice</span>
</p>
""", unsafe_allow_html=True)

# ========== MAIN FORM ==========
with st.form("quick_inquiry", clear_on_submit=True):
    st.markdown("### Get Your Quote")
    
    name = st.text_input("Your Name", placeholder="John Smith")
    phone = st.text_input("Phone Number", placeholder="(647) 521-6503")
    
    asset = st.selectbox("What are you storing?",
                        ["Select...", "RV / Motorhome", "Boat", 
                         "Commercial Truck", "Car / Trailer"],
                        index=0)
    
    size = st.select_slider("Size",
                           options=["Small", "Medium", "Large"],
                           value="Medium")
    
    months = st.number_input("How many months?", 
                            min_value=1, max_value=24, value=6)
    
    if asset != "Select...":
        rates = {"Small": 70, "Medium": 95, "Large": 125}
        base = rates.get(size, 95)
        if months >= 12:
            base = int(base * 0.85)
        elif months >= 6:
            base = int(base * 0.90)
        
        total = base * months
        st.success("Estimated: ${}/mo (${} total)".format(base, total))
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
            
            try:
                sender = st.secrets.get("smtp_email", "your-email@gmail.com")
                pwd = st.secrets.get("smtp_password", "your-password")
                
                msg = MIMEText("New Inquiry:\nName: {}\nPhone: {}\nAsset: {}\nSize: {}\nMonths: {}\nQuote: ${}".format(
                    name, phone, asset, size, months, st.session_state.get('calculated_quote', 0)))
                msg['Subject'] = "New Lead: {}".format(name)
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

# ========== PRICING ==========
with st.expander("View Full Pricing"):
    st.markdown("""
    **Small** (0-20ft): $60-80/mo  
    **Medium** (21-30ft): $80-110/mo  
    **Large** (31-40ft): $110-140/mo  
    
    *Winter storage (Oct-Apr): +25%*  
    *12-month prepay: 15% off*
    """)

# ========== TRUST BADGES ==========
st.markdown("""
<div style="display: flex; justify-content: space-around; margin: 30px 0; text-align: center; font-size: 12px; color: #666;">
    <div>24/7 Access<br>Available</div>
    <div>Gated &<br>Secure</div>
    <div>Instant<br>Quotes</div>
</div>
""", unsafe_allow_html=True)

# ========== SALLY CHATBOT ==========
st.markdown("---")
st.markdown("### Chat with Sally")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm Sally. Ask me about sizes, pricing, or availability!"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask Sally..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    prompt_lower = prompt.lower()
    
    if "price" in prompt_lower or "cost" in prompt_lower or "rate" in prompt_lower:
        response = "Our rates start at $60/month for small units and go up to $140 for large units. Winter months (Oct-Apr) have a 25% premium. How big is your vehicle?"
    elif "size" in prompt_lower or "big" in prompt_lower or "fit" in prompt_lower:
        response = "We accommodate everything from compact cars to large RVs up to 40ft. Our spots are sized: Small (0-20ft), Medium (21-30ft), and Large (31-40ft). What are you storing?"
    elif "available" in prompt_lower or "spot" in prompt_lower or "now" in prompt_lower:
        response = "We currently have spots open! Call me at {} or WhatsApp {} for immediate availability. I can hold a spot for 24 hours with a deposit.".format(FORMATTED_PHONE, WHATSAPP_NUMBER)
    elif "electric" in prompt_lower or "power" in prompt_lower:
        response = "Yes! We offer electricity hookups for $35/month. Perfect for keeping RV batteries charged or boat systems maintained."
    elif "location" in prompt_lower or "where" in prompt_lower or "address" in prompt_lower:
        response = "We're located in Ontario with easy highway access. I'll text you the exact address and gate code once you submit the form above!"
    elif "hour" in prompt_lower or "access" in prompt_lower or "gate" in prompt_lower:
        response = "Standard access is 6AM-10PM daily. We offer 24/7 access upgrade for $17/month if you need late night entry."
    else:
        response = "I'm here to help! For the fastest response, call me at {} or WhatsApp {}. You can also fill out the quote form above and I'll call you back within 10 minutes.".format(FORMATTED_PHONE, WHATSAPP_NUMBER)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)

# ========== STICKY FOOTER ==========
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

st.markdown("""
<div class="sticky-contact">
    <a href="tel:+1{}" class="sticky-btn" style="background: #333;">
        CALL {}
    </a>
    <a href="https://wa.me/1{}?text=Hi%20Sally,%20I%20need%20a%20storage%20quote" 
       class="sticky-btn" style="background: #25D366;">
        WHATSAPP
    </a>
</div>
""".format(PHONE_NUMBER, FORMATTED_PHONE, WHATSAPP_NUMBER), unsafe_allow_html=True)
