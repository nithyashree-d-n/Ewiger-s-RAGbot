import streamlit as st
import requests

# Top of streamlit_app.py
st.set_page_config(page_title="Ewiger: Secure RAG Chat", layout="centered")

st.title("🛡️ Ewiger: Secure Corporate Assistant")

st.sidebar.header("Login")

# Sidebar for credentials
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask me anything about company data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call our FastAPI backend
        with st.chat_message("assistant"):
            try:
                # Using 'params' instead of an f-string handles spaces/special characters automatically
                response = requests.post(
                    "http://127.0.0.1:8000/chat", 
                    params={"message": prompt}, 
                    auth=(username, password),
                    timeout=10 # Stop waiting after 10 seconds
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data['answer']
                    sources = ", ".join(data['sources'])
                    full_response = f"{answer}\n\n**Sources:** {sources}"
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                elif response.status_code == 401:
                    st.error("🚫 Access Denied: Invalid Username or Password.")
                
                elif response.status_code == 500:
                    st.error("🧠 The Brain (Backend) had an internal error. Check your .env/Groq key.")

            except requests.exceptions.ConnectionError:
                st.error("🔌 Connection Failed: Is the FastAPI server running on port 8000?")
            except Exception as e:
                st.error(f"⚠️ Unexpected Error: {e}")
