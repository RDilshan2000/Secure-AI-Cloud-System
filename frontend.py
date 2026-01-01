import streamlit as st
import requests

# --- Settings ---
API_URL = "https://secure-ai-cloud-system.onrender.com"  # ඔයාගේ Backend Link එක
st.set_page_config(page_title="Secure AI Vault", page_icon="🛡️", layout="wide")

# --- Styles ---
st.markdown("""
    <style>
    .stApp {background-color: #0e1117; color: white;}
    .stTextInput > div > div > input {background-color: #262730; color: white;}
    .stTextArea > div > div > textarea {background-color: #262730; color: white;}
    .stButton > button {background-color: #00ff41; color: black; font-weight: bold;}
    .success-box {padding: 1rem; background-color: #00441b; border-left: 5px solid #00ff41; border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)

# --- Session Management ---
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("🛡️ Secure Vault")
    st.caption("Enterprise AI Cloud System")
    st.divider()
    
    if st.session_state.token:
        st.success(f"🟢 Online: {st.session_state.username}")
        page = st.radio("Navigate", ["🤖 AI Analyzer", "📜 Past Scans", "👤 My Profile"])
        
        st.divider()
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.username = None
            st.rerun()
    else:
        st.warning("🔴 Offline")
        page = "Login"

# --- LOGIN / SIGNUP PAGE ---
if not st.session_state.token:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=150)
    with col2:
        st.header("Access Control")
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Signup"])
        
        with tab1:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Unlock Vault 🔓"):
                try:
                    res = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.token = data["access_token"]
                        st.session_state.username = username
                        st.toast("Access Granted!", icon="✅")
                        st.rerun()
                    else:
                        st.error("Access Denied: Invalid Credentials")
                except:
                    st.error("Server Connection Failed")

        with tab2:
            new_user = st.text_input("Choose Username", key="sign_user")
            new_pass = st.text_input("Choose Password", type="password", key="sign_pass")
            if st.button("Create ID 🆔"):
                try:
                    res = requests.post(f"{API_URL}/signup", json={"username": new_user, "password": new_pass})
                    if res.status_code == 200:
                        st.success("Identity Created! Please Login.")
                    else:
                        st.error("Username already taken.")
                except:
                    st.error("Server Error")

# --- MAIN APP PAGES ---
elif page == "🤖 AI Analyzer":
    st.header("🧠 Intelligence Center")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Source Data")
        input_text = st.text_area("Paste confidential notes here...", height=300)
        if st.button("⚡ Process Data"):
            if input_text:
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                payload = {"username": st.session_state.username, "text": input_text}
                
                with st.spinner("Encrypting & Analyzing..."):
                    try:
                        res = requests.post(f"{API_URL}/analyze", json=payload, headers=headers)
                        if res.status_code == 200:
                            summary = res.json().get("summary")
                            st.session_state.latest_summary = summary
                        else:
                            st.error(f"Error: {res.status_code}")
                    except Exception as e:
                        st.error(f"Connection Error: {e}")

    with col2:
        st.subheader("📤 Intelligence Output")
        if "latest_summary" in st.session_state:
            st.markdown(f"""
                <div class="success-box">
                    <h4>✨ Executive Summary:</h4>
                    <p>{st.session_state.latest_summary}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Waiting for input data...")

elif page == "📜 Past Scans":
    st.header("🗄️ Scan History Archive")
    st.caption(f"Showing protected records for: {st.session_state.username}")
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    try:
        # Backend එකෙන් History එක ඉල්ලනවා
        res = requests.get(f"{API_URL}/history/{st.session_state.username}", headers=headers)
        
        if res.status_code == 200:
            history_data = res.json()
            
            if not history_data:
                st.info("No records found in the vault.")
            else:
                for item in reversed(history_data):
                    with st.expander(f"🕒 {item['timestamp']} - Summary"):
                        st.success(f"**AI Summary:** {item['summary_text']}")
                        st.code(f"Original: {item['original_text']}", language="text")
        else:
            st.error("Failed to fetch history.")
    except Exception as e:
        st.error(f"Connection Error: {e}")

elif page == "👤 My Profile":
    st.header("User Profile")
    st.markdown(f"**Officer Name:** {st.session_state.username}")
    st.markdown("**Security Clearance:** Level 5 (Top Secret)")
    st.image("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDdtYmxuYmF6YjFqaXJ6b2F6YjFqaXJ6b2F6YjFqaXJ6b2F6YjFqaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YNX1JtT1hI16J7r2r0/giphy.gif", width=300)