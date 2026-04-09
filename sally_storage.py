import streamlit as st
import smtplib
import sqlite3
import json
import base64
import uuid
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Try to import OpenAI, but don't crash if it's missing
try:
    from openai import OpenAI
    client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", "demo-key")))
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    client = None

# Try to import PIL
try:
    from PIL import Image
    import io
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="PRESTIGE ENTERPRISES | Premium Storage Solutions",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Database setup
DB_PATH = "prestige_memory.db"

def init_db():
    """Initialize database with all tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_asset_type TEXT,
            last_dimensions TEXT,
            last_quote REAL,
            conversation_count INTEGER DEFAULT 0,
            preferences TEXT
        );
        
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            message TEXT,
            response TEXT,
            image_analyzed INTEGER DEFAULT 0,
            estimated_length REAL,
            asset_type TEXT,
            quote_amount REAL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );
        
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            asset_type TEXT,
            dimensions TEXT,
            duration_months INTEGER,
            estimated_quote REAL,
            message TEXT,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS inventory (
            date TEXT PRIMARY KEY,
            rv_spots INTEGER,
            boat_spots INTEGER,
            container_spots INTEGER,
            truck_spots INTEGER,
            car_spots INTEGER,
            seasonal_factor TEXT
        );
    ''')
    
    # Seed predictive data
    months = ['2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06',
              '2026-07', '2026-08', '2026-09', '2026-10', '2026-11', '2026-12']
    
    patterns = {
        '01': (80, 40, 60, 50, 70, 'winter_peak'),
        '02': (85, 45, 65, 55, 75, 'winter_peak'),
        '03': (75, 50, 70, 60, 80, 'spring_transition'),
        '04': (60, 65, 75, 65, 85, 'spring'),
        '05': (40, 80, 70, 70, 90, 'boating_season'),
        '06': (30, 95, 75, 75, 95, 'summer_peak'),
        '07': (25, 90, 80, 80, 90, 'summer_peak'),
        '08': (30, 85, 85, 85, 85, 'summer'),
        '09': (50, 70, 75, 75, 80, 'fall'),
        '10': (70, 50, 70, 60, 75, 'winter_prep'),
        '11': (85, 40, 65, 55, 70, 'winter_peak'),
        '12': (90, 35, 60, 50, 65, 'winter_peak')
    }
    
    for month in months:
        key = month.split('-')[1]
        rv, boat, cont, truck, car, factor = patterns[key]
        
        c.execute('''INSERT OR IGNORE INTO inventory 
                     (date, rv_spots, boat_spots, container_spots, truck_spots, car_spots, seasonal_factor)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (month, 100-rv, 100-boat, 100-cont, 100-truck, 100-car, factor))
    
    conn.commit()
    conn.close()

init_db()

# ==================== PRICING ENGINE ====================
def calculate_quote(category, duration_months, season="standard", addons=None, fleet_size=1):
    """Dynamic pricing calculator"""
    base_rates = {
        'small': 70,
        'medium': 95,
        'large': 125,
        'xl': 160,
        'container': 215
    }
    
    if category not in base_rates:
        return None
    
    base = base_rates[category]
    
    seasonal_multipliers = {
        'winter': 1.25,
        'summer': 0.90,
        'standard': 1.0
    }
    
    base *= seasonal_multipliers.get(season, 1.0)
    
    if duration_months >= 12:
        base *= 0.85
    elif duration_months >= 6:
        base *= 0.90
    elif duration_months == 1:
        base *= 1.1
    
    if fleet_size >= 10:
        base *= 0.85
    elif fleet_size >= 6:
        base *= 0.90
    elif fleet_size >= 3:
        base *= 0.95
    
    addon_total = 0
    if addons:
        if 'electricity' in addons:
            addon_total += 35
        if '24_7_access' in addons:
            addon_total += 17
        if 'premium_spot' in addons:
            addon_total += 22
        if 'cover' in addons:
            addon_total += 45
    
    total = (base + addon_total) * fleet_size
    
    return {
        'base_monthly': round(base, 2),
        'addons_monthly': round(addon_total, 2),
        'total_monthly': round(base + addon_total, 2),
        'total_duration': round((base + addon_total) * duration_months, 2),
        'savings': round((base_rates[category] * duration_months) - (base * duration_months), 2),
        'season_applied': season,
        'discount_tier': 'Fleet' if fleet_size > 1 else 'Long-term' if duration_months >= 6 else 'Standard'
    }

# ==================== EMAIL SYSTEM ====================
def send_inquiry_email(name, email, phone, asset_type, dimensions, duration, message, quote=None):
    """Send inquiry via SMTP"""
    try:
        sender = st.secrets.get("smtp_email", "prestige.inquiries@gmail.com")
        password = st.secrets.get("smtp_password", "your-app-password")
        receiver = "greguhl33@gmail.com"
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = "NEW INQUIRY: {} - {}".format(name, asset_type or 'General')
        
        quote_text = ""
        if quote:
            quote_text = "<p><strong>Estimated Quote:</strong> ${} (${}/mo)</p>".format(
                quote['total_duration'], quote['total_monthly'])
        
        body = """
        <html>
        <body style="font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px;">
            <div style="max-width: 600px; background: white; padding: 30px; border-left: 5px solid #000;">
                <h2 style="margin-top: 0; color: #000;">PRESTIGE ENTERPRISES</h2>
                <h3 style="color: #333;">New Storage Inquiry Received</h3>
                
                <table style="width: 100%; border-collapse: collapse;">
                    <tr><td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Name:</strong></td><td>{}</td></tr>
                    <tr><td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Email:</strong></td><td>{}</td></tr>
                    <tr><td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Phone:</strong></td><td>{}</td></tr>
                    <tr><td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Asset Type:</strong></td><td>{}</td></tr>
                    <tr><td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Dimensions:</strong></td><td>{}</td></tr>
                    <tr><td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Duration:</strong></td><td>{} months</td></tr>
                </table>
                
                {}
                
                <h4 style="margin-top: 20px;">Message:</h4>
                <p style="background: #f9f9f9; padding: 15px; border-left: 3px solid #ccc;">{}</p>
                
                <p style="margin-top: 30px; font-size: 12px; color: #666;">
                    Received: {}<br>
                    <a href="mailto:{}?subject=Re: Your Storage Inquiry">Reply to customer</a>
                </p>
            </div>
        </body>
        </html>
        """.format(name, email, phone, asset_type or 'Not specified', 
                   dimensions or 'Not specified', duration or 'Not specified',
                   quote_text, message, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), email)
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
        
        return True, "Inquiry sent successfully. We'll contact you within 24 hours."
    except Exception as e:
        return False, "Email error: {}".format(str(e))

# ==================== AI VISION ANALYSIS ====================
def analyze_vehicle_image(image_file):
    """Analyze uploaded vehicle image"""
    if not AI_AVAILABLE or not PIL_AVAILABLE:
        return None
    
    try:
        image = Image.open(image_file)
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a vehicle dimension expert. Analyze the image and return ONLY JSON: {vehicle_type, estimated_length_feet, confidence, size_category, notable_features, notes}"
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,{}".format(img_str)}}
                    ]
                }
            ],
            max_tokens=300
        )
        
        content = response.choices[0].message.content
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        
        return json.loads(content)
    except:
        return None

# ==================== PREDICTIVE ANALYTICS ====================
def get_predictive_warning(asset_type):
    """Check availability based on historical data"""
    now = datetime.now()
    month_key = now.strftime('%Y-%m')
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM inventory WHERE date = ?', (month_key,))
    data = c.fetchone()
    conn.close()
    
    if not data:
        return None
    
    warnings = []
    urgency = 0
    
    asset_map = {'rv': 1, 'boat': 2, 'container': 3, 'truck': 4, 'car': 5}
    idx = asset_map.get(asset_type, 0)
    spots = data[idx] if idx > 0 else 50
    
    if spots < 20:
        urgency = 50
        warnings.append("ALERT: Only ~{} {} spots remain for {}".format(spots, asset_type, month_key))
    
    if asset_type == 'rv' and data[6] == 'winter_peak':
        warnings.append("URGENT: Winter storage rush. Book today to avoid waitlist.")
    
    if asset_type == 'boat' and data[6] == 'summer_peak':
        warnings.append("PEAK SEASON: 95% capacity on weekends historically.")
    
    return {'urgency': urgency, 'warnings': warnings, 'spots_left': spots}

# ==================== USER MEMORY ====================
def get_user_memory(user_id):
    """Retrieve user context"""
    if not user_id:
        return None
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    user = c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    
    if user:
        last_date = datetime.fromisoformat(user[6]) if user[6] else None
        days_away = (datetime.now() - last_date).days if last_date else 0
        
        return {
            'is_returning': True,
            'name': user[1],
            'email': user[2],
            'days_away': days_away,
            'last_asset': user[7],
            'last_dimensions': user[8],
            'conversation_count': user[10]
        }
    return None

def update_memory(user_id, **kwargs):
    """Update user memory"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    
    fields = []
    values = []
    for key, val in kwargs.items():
        fields.append("{} = ?".format(key))
        values.append(val)
    
    fields.append("last_visit = ?")
    values.append(now)
    values.append(user_id)
    
    c.execute("UPDATE users SET {} WHERE user_id = ?".format(', '.join(fields)), values)
    
    if c.rowcount == 0:
        c.execute('INSERT INTO users (user_id, created_at) VALUES (?, ?)', (user_id, now))
    
    conn.commit()
    conn.close()

# ==================== UI COMPONENTS ====================
def inject_css():
    """Custom CSS for luxury black/white theme"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;600&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            color: #ffffff;
        }
        
        .main-header {
            font-family: 'Playfair Display', serif;
            font-size: 48px;
            font-weight: 900;
            text-align: center;
            letter-spacing: 8px;
            text-transform: uppercase;
            margin: 20px 0;
            background: linear-gradient(to bottom, #ffffff, #a0a0a0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            border-bottom: 3px solid #333;
            padding-bottom: 20px;
        }
        
        .sub-header {
            font-family: 'Inter', sans-serif;
            text-align: center;
            color: #888;
            letter-spacing: 4px;
            text-transform: uppercase;
            font-size: 14px;
            margin-bottom: 40px;
        }
        
        .pp-logo {
            text-align: center;
            font-family: 'Playfair Display', serif;
            font-size: 72px;
            font-weight: 900;
            letter-spacing: -10px;
            color: #ffffff;
            text-shadow: 3px 3px 0px #333;
            margin: 20px 0;
        }
        
        .pp-logo span {
            display: inline-block;
            transform: skewX(-15deg);
            border: 3px solid #fff;
            padding: 0 20px;
            margin: 0 -5px;
        }
        
        .stButton>button {
            background: #ffffff !important;
            color: #000000 !important;
            font-weight: bold !important;
            border: none !important;
            border-radius: 0 !important;
            height: 50px !important;
            font-family: 'Inter', sans-serif !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
        }
        
        .stButton>button:hover {
            background: #cccccc !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(255,255,255,0.2);
        }
        
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background: #1a1a1a !important;
            color: #ffffff !important;
            border: 1px solid #333 !important;
            border-radius: 0 !important;
        }
        
        .price-box {
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
            border-left: 4px solid #fff;
            padding: 20px;
            margin: 10px 0;
        }
        
        .urgency-banner {
            background: linear-gradient(90deg, #dc2626, #991b1b);
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: bold;
            margin: 20px 0;
            border-left: 5px solid #fff;
        }
        
        .chat-message {
            background: #1a1a1a;
            border: 1px solid #333;
            padding: 15px;
            margin: 10px 0;
            border-radius: 0;
        }
        
        #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==================== MAIN APP ====================
def main():
    inject_css()
    
    # User ID for memory
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    
    user_id = st.session_state.user_id
    user_memory = get_user_memory(user_id)
    
    # Header with PP Logo
    st.markdown('<div class="pp-logo"><span>P</span><span>P</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">PRESTIGE ENTERPRISES</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Premium Outdoor Storage Solutions   Ontario</div>', unsafe_allow_html=True)
    
    # Sidebar - Special Powers
    with st.sidebar:
        st.markdown("### Sally AI Powers")
        st.markdown("---")
        
        # Vision Upload
        uploaded_file = st.file_uploader("Upload Vehicle Photo", type=['jpg', 'png', 'jpeg'])
        vision_data = None
        
        if uploaded_file:
            with st.spinner("Analyzing..."):
                vision_data = analyze_vehicle_image(uploaded_file)
                if vision_data:
                    st.success("Detected: {}".format(vision_data['vehicle_type']))
                    st.info("Estimated: {}ft".format(vision_data['estimated_length_feet']))
                    st.session_state['vision_context'] = vision_data
        
        # Quick Calculator
        st.markdown("### Quick Quote")
        asset_type = st.selectbox("Asset", ["RV", "Boat", "Container", "Truck", "Car"])
        size = st.select_slider("Size", options=["Small", "Medium", "Large", "X-Large"])
        months = st.slider("Duration (months)", 1, 12, 6)
        
        cat_map = {"Small": "small", "Medium": "medium", "Large": "large", "X-Large": "xl"}
        season = "winter" if datetime.now().month in [10, 11, 12, 1, 2, 3] else "standard"
        
        quote = calculate_quote(cat_map[size], months, season)
        if quote:
            st.metric("Monthly Rate", "${}".format(quote['total_monthly']))
            st.metric("Total Cost", "${}".format(quote['total_duration']))
            if quote['savings'] > 0:
                st.success("Save ${}!".format(quote['savings']))
        
        # Predictive Warning
        pred = get_predictive_warning(asset_type.lower())
        if pred and pred['warnings']:
            st.markdown("### Availability Alert")
            for w in pred['warnings']:
                st.warning(w)
    
    # Main Content Columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Welcome for returning users
        if user_memory and user_memory['is_returning']:
            st.info("Welcome back, {}! Last time you were interested in {} storage.".format(
                user_memory['name'] or 'valued client', user_memory['last_asset']))
        
        st.markdown("### Storage Inquiry")
        
        with st.form("inquiry_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name*", value=user_memory['name'] if user_memory else "")
                email = st.text_input("Email Address*")
            with c2:
                phone = st.text_input("Phone Number")
                asset = st.selectbox("Asset Type", ["", "RV / Motorhome", "Boat / Marine", "Shipping Container", "Commercial Truck", "Car / SUV", "Other"])
            
            dimensions = st.text_input("Dimensions (L x W x H) or Vehicle Length", placeholder="e.g., 35 feet")
            duration = st.number_input("Storage Duration (months)", min_value=1, max_value=24, value=6)
            
            # Auto-calculate if vision data exists
            auto_quote = None
            if 'vision_context' in st.session_state:
                v = st.session_state['vision_context']
                cat = v.get('size_category', 'medium')
                auto_quote = calculate_quote(cat, duration, season)
                st.success("AI Detected: {} ({}ft) - Estimated Category: {}".format(
                    v['vehicle_type'], v['estimated_length_feet'], cat))
            
            message = st.text_area("Additional Details", placeholder="Tell us about access requirements, electrical needs, etc.")
            
            submit = st.form_submit_button("SUBMIT INQUIRY")
            
            if submit:
                if name and email and asset:
                    # Determine category
                    cat = "medium"
                    if "RV" in asset:
                        cat = "large"
                    elif "Container" in asset:
                        cat = "container"
                    elif "Truck" in asset:
                        cat = "xl"
                    
                    final_quote = auto_quote or calculate_quote(cat, duration, season)
                    
                    success, msg = send_inquiry_email(
                        name, email, phone, asset, dimensions, duration, message, final_quote
                    )
                    
                    if success:
                        st.success(msg)
                        # Save to memory
                        update_memory(user_id, name=name, email=email, last_asset_type=asset, 
                                    last_dimensions=dimensions, last_quote=final_quote['total_duration'])
                        
                        # Save inquiry to DB
                        conn = sqlite3.connect(DB_PATH)
                        c = conn.cursor()
                        c.execute('''INSERT INTO inquiries 
                                     (name, email, phone, asset_type, dimensions, duration_months, estimated_quote, message)
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                  (name, email, phone, asset, dimensions, duration, 
                                   final_quote['total_duration'] if final_quote else None, message))
                        conn.commit()
                        conn.close()
                    else:
                        st.error(msg)
                        st.info("Please email us directly at greguhl33@gmail.com")
                else:
                    st.warning("Please fill in required fields (Name, Email, Asset Type)")
    
    with col2:
        st.markdown("### 2026 Pricing")
        pricing_data = """
        **Small** (up to 20ft): $60-80/mo  
        **Medium** (21-30ft): $80-110/mo  
        **Large** (31-40ft): $110-140/mo  
        **XL** (41-50ft): $140-180/mo  
        **Container** (50ft+): $180-250/mo
        
        ---
        **Add-ons:**
        Electricity: +$35/mo  
        24/7 Access: +$17/mo  
        Premium Spot: +$22/mo
        
        ---
        **Seasonal:**
        Winter (Oct-Apr): +25%  
        Summer Discount: -10%
        """
        st.markdown(pricing_data)
        
        if st.button("Download Price Sheet"):
            st.download_button(
                label="Click to Download",
                data="Prestige Enterprises Pricing 2026\n\nStandard Rates...\n(Placeholder for actual PDF)",
                file_name="prestige_pricing_2026.txt",
                mime="text/plain"
            )
    
    st.divider()
    
    # Chatbot Section
    st.markdown("### Chat with Sally")
    
    if "messages" not in st.session_state:
        welcome_msg = "Hello! I'm Sally, your AI storage consultant. I can analyze vehicle photos, calculate exact quotes, and check real-time availability. What are you storing today?"
        if user_memory and user_memory['is_returning']:
            welcome_msg = "Welcome back! Last time you were looking at {} storage. Shall we find you that spot?".format(
                user_memory['last_asset'])
        
        st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]
    
    # Display chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask Sally about storage..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Intent detection
        prompt_lower = prompt.lower()
        
        # Simple response logic
        if "price" in prompt_lower or "cost" in prompt_lower:
            reply = "Our 2026 rates range from $60-250/month depending on size. Small units start at $60, RVs at $125, and containers at $180. Winter storage (Oct-Apr) carries a 25% premium due to demand. Would you like me to calculate a specific quote?"
        elif "available" in prompt_lower or "spot" in prompt_lower:
            pred = get_predictive_warning('rv')
            if pred and pred['urgency'] > 40:
                reply = "High demand alert! We currently have limited spots. {} I recommend submitting an inquiry immediately to reserve.".format(
                    pred['warnings'][0] if pred['warnings'] else '')
            else:
                reply = "We have spots available! Submit an inquiry above and I'll hold one for 24 hours with a $50 deposit."
        elif "electric" in prompt_lower or "power" in prompt_lower:
            reply = "We offer battery trickle charging for $35/month. This is perfect for RVs and boats to maintain batteries during long-term storage."
        else:
            # Fallback to OpenAI for complex queries if available
            if AI_AVAILABLE:
                try:
                    context = "User inquiry: {}. User history: {}".format(prompt, user_memory)
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are Sally from Prestige Enterprises. Be concise, professional, and push for form submission."},
                            {"role": "user", "content": context}
                        ]
                    )
                    reply = response.choices[0].message.content
                except:
                    reply = "For detailed questions, please fill out the inquiry form above or email greguhl33@gmail.com. I can also analyze a photo of your vehicle if you upload it in the sidebar!"
            else:
                reply = "For detailed questions, please fill out the inquiry form above or email greguhl33@gmail.com. I can also analyze a photo of your vehicle if you upload it in the sidebar!"
        
        with st.chat_message("assistant"):
            st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    main()

