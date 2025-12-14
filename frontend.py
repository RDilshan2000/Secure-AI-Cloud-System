import streamlit as st
import requests
from requests.exceptions import ConnectionError

# Page Config (Wide Layout + Title)
st.set_page_config(page_title="Secure AI Vault", page_icon="🛡️", layout="wide")

# Advanced Custom CSS (Glassmorphism & Neon Effects)
st.markdown("""
    <style>
    .stApp {
        background: rgb(15,15,15);
        background: linear-gradient(34deg, rgba(15,15,15,1) 0%, rgba(28,28,28,1) 35%, rgba(0,20,10,1) 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Buttons*/
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #00C853 0%, #64DD17 100%);
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 12px;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 15px rgba(0, 200, 83, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 20px rgba(0, 200, 83, 0.6);
        color: white;
    }

    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    /* Login/Profile Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 30px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Success Box (AI Summary) */
    .ai-result-box {
        background: rgba(0, 200, 83, 0.1);
        border-left: 5px solid #00C853;
        padding: 20px;
        border-radius: 10px;
        color: #e0e0e0;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    h1, h2, h3 { font-family: 'Segoe UI', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# Backend URL
API_URL = "https://secure-ai-cloud-system.onrender.com"

# Session State
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

# --- SIDEBAR DESIGN ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9131/9131546.png", width=80)
    st.title("Secure Vault")
    st.caption("Enterprise AI Cloud System")
    st.markdown("---")

    if st.session_state["access_token"]:
        st.success(f"🟢 Online: **{st.session_state['current_user']}**")
        menu = st.radio("Navigate", ["🤖 AI Analyzer", "👤 My Profile"])
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state["access_token"] = None
            st.session_state["current_user"] = None
            st.rerun()
    else:
        menu = st.radio("Menu", ["🔑 Login", "📝 Signup"])

# --- MAIN CONTENT ---

# 1. LOGIN PAGE
if menu == "🔑 Login":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        # Glass Card Effect for Login
        st.markdown('<div class="glass-card"><h2>🔐 Access Portal</h2><p>Enter your credentials to unlock the vault.</p></div>', unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.write("") # Gap
        if st.button("Unlock System 🔓"):
            payload = {"username": username, "password": password}
            try:
                with st.spinner("Authenticating..."):
                    response = requests.post(f"{API_URL}/token", data=payload)
                    if response.status_code == 200:
                        token = response.json()["access_token"]
                        st.session_state["access_token"] = token
                        st.session_state["current_user"] = username
                        st.toast("Access Granted!", icon="✅")
                        st.rerun()
                    else:
                        st.error("Access Denied! Incorrect Credentials.")
            except ConnectionError:
                st.error("🚨 System Failure: Backend is Offline")
            except Exception as e:
                st.error(f"Error: {e}")

# 2. SIGNUP PAGE
elif menu == "📝 Signup":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="glass-card"><h2>🚀 New Membership</h2><p>Join the secure network today.</p></div>', unsafe_allow_html=True)
        
        new_user = st.text_input("Choose Username")
        new_pass = st.text_input("Choose Password", type="password")
        
        st.write("")
        if st.button("Create ID 🆔"):
            payload = {"username": new_user, "password": new_pass}
            try:
                response = requests.post(f"{API_URL}/signup", json=payload)
                if response.status_code == 200:
                    st.balloons()
                    st.success("Identity Created Successfully! Please Login.")
                else:
                    st.warning("Username already exists in the vault.")
            except ConnectionError:
                st.error("Backend Offline")

# 3. AI ANALYZER
elif menu == "🤖 AI Analyzer":
    st.markdown("<h1>🧠 Neural Analyzer <span style='font-size:20px; color:gray'>v2.0</span></h1>", unsafe_allow_html=True)
    st.caption("Securely processed by HuggingFace Transformers (Running on Local Cloud)")
    st.markdown("---")

    col_input, col_output = st.columns(2)

    with col_input:
        st.subheader("📥 Source Data")
        user_input = st.text_area("Paste confidential notes here...", height=350)
        st.write("")
        analyze_btn = st.button("⚡ Process Data")

    with col_output:
        st.subheader("📤 Intelligence Output")
        
        if analyze_btn:
            if user_input:
                headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
                payload = {"content": user_input}
                
                with st.spinner("🔄 Decrypting & Analyzing..."):
                    try:
                        response = requests.post(f"{API_URL}/analyze_note", json=payload, headers=headers)
                        if response.status_code == 200:
                            data = response.json()
                            # Custom HTML result box
                            st.markdown(f"""
                                <div class="ai-result-box">
                                    <h4 style="margin-top:0">✨ Executive Summary:</h4>
                                    <p>{data['ai_summary']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            with st.expander("🔍 Metadata"):
                                st.code(f"User ID: {data['user']}\nChars: {len(user_input)}\nStatus: Secure", language="yaml")
                        else:
                            st.error("Session Token Expired. Login required.")
                    except:
                        st.error("Communication Breakdown!")
            else:
                st.warning("Input buffer is empty.")
        else:
            # Placeholder when no result
            st.markdown("""
                <div style="border: 2px dashed rgba(255,255,255,0.1); border-radius:10px; height:350px; display:flex; align-items:center; justify-content:center; color:gray;">
                    Waiting for analysis trigger...
                </div>
            """, unsafe_allow_html=True)

# 4. PROFILE
elif menu == "👤 My Profile":
    col1, col2 = st.columns([1, 2])
    with col1:
        # Profile Picture Placeholder
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
    
    with col2:
        st.title(f"Commander {st.session_state['current_user']}")
        st.markdown('<span style="background-color:#00C853; color:black; padding:5px 10px; border-radius:5px; font-weight:bold">ADMIN CLEARANCE</span>', unsafe_allow_html=True)
        
        st.write("")
        st.write("Welcome to your secure dashboard. All systems are operational.")
        
        # Stats
        c1, c2, c3 = st.columns(3)
        c1.metric("Security Level", "High", "100%")
        c2.metric("System Uptime", "99.9%", "+0.4%")