import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Secure AI Vault", page_icon="🔒")
st.title("🔒 Secure AI Vault - Cloud System")

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

menu = st.sidebar.selectbox("Menu", ["Login 🔑", "Signup 📝", "AI Analyzer 🧠"])

if menu == "Login 🔑":
    st.subheader("Login to your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        payload = {"username": username, "password": password}
        try:
            response = requests.post(f"{API_URL}/token", data=payload)
            
            if response.status_code == 200:
                token = response.json()["access_token"]
                st.session_state["access_token"] = token
                st.success("Login Successful! Now go to 'AI Analyzer' tab. ✅")
            else:
                st.error("Login Failed! Check username or password. ❌")
        except:
            st.error("Error: Is the Backend Server running? ⚠️")

elif menu == "Signup 📝":
    st.subheader("Create New Account")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    
    if st.button("Create Account"):
        payload = {"username": new_user, "password": new_pass}
        try:
            response = requests.post(f"{API_URL}/signup", json=payload)
            if response.status_code == 200:
                st.success("Account Created! Please Login now. 🎉")
            else:
                st.error("Error: Username might be taken.")
        except:
            st.error("Connection Error ⚠️")

elif menu == "AI Analyzer 🧠":
    if st.session_state["access_token"]:
        st.subheader("Welcome to the Secure AI Zone")
        
        user_input = st.text_area("Paste your long text here to summarize:", height=200)
        
        if st.button("Analyze with AI 🚀"):
            if user_input:
                headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
                payload = {"content": user_input}
                
                with st.spinner("AI is thinking... 🤔"):
                    try:
                        response = requests.post(f"{API_URL}/analyze_note", json=payload, headers=headers)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.info(f"User: {data['user']}")
                            st.success(f"📝 AI Summary: {data['ai_summary']}")
                        else:
                            st.error("Session Expired. Please Login again.")
                    except:
                        st.error("Connection Error ⚠️")
            else:
                st.warning("Please enter some text first.")
    else:
        st.warning("⚠️ You need to Login first to access this area!")