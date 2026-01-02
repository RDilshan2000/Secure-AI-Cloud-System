import streamlit as st
import requests


API_URL = "https://secure-ai-cloud-system.onrender.com"  
st.set_page_config(page_title="Secure AI Vault", page_icon="🛡️", layout="wide")


st.markdown("""
    <style>
    .stApp {background-color: #0e1117; color: white;}
    .stTextInput > div > div > input {background-color: #262730; color: white;}
    .stButton > button {width: 100%; border-radius: 5px; font-weight: bold;}
    .success-box {padding: 1rem; background-color: #00441b; border-left: 5px solid #00ff41; border-radius: 5px; margin-bottom: 10px;}
    .mood-box {padding: 1rem; background-color: #1a237e; border-left: 5px solid #536dfe; border-radius: 5px; margin-bottom: 10px;}
    .user-card {padding: 10px; background-color: #262730; border-radius: 5px; margin-bottom: 5px; border: 1px solid #444;}
    </style>
""", unsafe_allow_html=True)


if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None


with st.sidebar:
    st.title("🛡️ Secure Vault")
    st.caption("Enterprise AI Cloud System")
    st.divider()
    
    if st.session_state.token:
        st.success(f"🟢 Online: {st.session_state.username}")
        
        menu_options = ["🤖 AI Analyzer", "📜 Past Scans", "👮‍♂️ Admin Panel", "👤 My Profile"]
        page = st.radio("Navigate", menu_options)
        
        st.divider()
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.username = None
            st.rerun()
    else:
        st.warning("🔴 Offline")
        page = "Login"


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


elif page == "🤖 AI Analyzer":
    st.header("🧠 Intelligence Center")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Source Data")
        input_text = st.text_area("Paste text here...", height=300)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("⚡ Summarize"):
                if input_text:
                    headers = {"Authorization": f"Bearer {st.session_state.token}"}
                    payload = {"username": st.session_state.username, "text": input_text}
                    with st.spinner("Processing..."):
                        try:
                            res = requests.post(f"{API_URL}/analyze", json=payload, headers=headers)
                            if res.status_code == 200:
                                st.session_state.result_type = "summary"
                                st.session_state.result_data = res.json().get("summary")
                            else:
                                st.error(f"Error: {res.text}")
                        except Exception as e:
                            st.error(f"Error: {e}")

        with btn_col2:
            if st.button("🎭 Analyze Mood"):
                if input_text:
                    headers = {"Authorization": f"Bearer {st.session_state.token}"}
                    payload = {"username": st.session_state.username, "text": input_text}
                    with st.spinner("Detecting Emotions..."):
                        try:
                            res = requests.post(f"{API_URL}/sentiment", json=payload, headers=headers)
                            if res.status_code == 200:
                                st.session_state.result_type = "mood"
                                st.session_state.result_data = res.json().get("result")
                            else:
                                st.error(f"Error: {res.text}")
                        except Exception as e:
                            st.error(f"Error: {e}")

    with col2:
        st.subheader("📤 Output Result")
        if "result_data" in st.session_state:
            if st.session_state.result_type == "summary":
                st.markdown(f"""<div class="success-box"><h4>📝 Summary:</h4><p>{st.session_state.result_data}</p></div>""", unsafe_allow_html=True)
            elif st.session_state.result_type == "mood":
                st.markdown(f"""<div class="mood-box"><h4>🎭 Detected Mood:</h4><h2>{st.session_state.result_data}</h2></div>""", unsafe_allow_html=True)
        else:
            st.info("Waiting for input...")


elif page == "📜 Past Scans":
    st.header("🗄️ Scan History Archive")
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    try:
        res = requests.get(f"{API_URL}/history/{st.session_state.username}", headers=headers)
        if res.status_code == 200:
            history_data = res.json()
            if not history_data:
                st.info("No records found.")
            else:
                for item in reversed(history_data):
                    with st.expander(f"🕒 {item['timestamp']} - Record"):
                        st.info(f"**Result:** {item['summary_text']}")
                        st.text(f"Original: {item['original_text']}")
        else:
            st.error("Failed to fetch history.")
    except Exception as e:
        st.error(f"Connection Error: {e}")


elif page == "👮‍♂️ Admin Panel":
    st.header("🔒 Admin Control Panel")
    st.info("Manage all registered users in the system.")
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    if st.button("🔄 Refresh User List"):
        st.rerun()
        
    try:
        res = requests.get(f"{API_URL}/users", headers=headers)
        if res.status_code == 200:
            users = res.json()
            st.write(f"**Total Users:** {len(users)}")
            
            for user in users:
                
                c1, c2 = st.columns([4, 1])
                
                with c1:
                    st.markdown(f"<div class='user-card'>👤 <b>{user['username']}</b></div>", unsafe_allow_html=True)
                
                with c2:
                    if user['username'] != st.session_state.username:
                        if st.button("🗑️ Delete", key=f"del_{user['username']}"):
                            del_res = requests.delete(f"{API_URL}/users/{user['username']}", headers=headers)
                            if del_res.status_code == 200:
                                st.success(f"User Deleted!")
                                st.rerun()
                            else:
                                st.error("Failed")
                    else:
                        st.caption("(You)")
        else:
            st.error("Failed to load users.")
    except Exception as e:
        st.error(f"Error: {e}")


elif page == "👤 My Profile":
    st.header("User Profile")
    st.markdown(f"**Officer Name:** {st.session_state.username}")
    st.markdown("**Role:** Administrator")
    st.image("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDdtYmxuYmF6YjFqaXJ6b2F6YjFqaXJ6b2F6YjFqaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YNX1JtT1hI16J7r2r0/giphy.gif", width=300)