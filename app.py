import streamlit as st
import requests

st.set_page_config(page_title = "House Prediction", page_icon = "🤟🏼", layout = "wide")

def login (username: str, password: str):
    url = "http://127.0.0.1:8000/api/v1/login"
    try:
        response = requests.post(url, 
                                data = {"username": username, "password": password},
                                headers={"Content-Type": "application/x-www-form-urlencoded"},
                                timeout = 10)
        
        response.raise_for_status()
        return response.json()

    except Exception as err:
        return {"error": str(err)}
    
with st.sidebar:

    st.title("🔒 Login")

    st.markdown("---")

    username = st.text_input("Username", type = "default")
    password = st.text_input("Senha", type = "password")

    button = st.button("Login")

    if button and (username and password):
        result = login(username, password)
        if "error" in result:
            st.sidebar.error("Credencias inválidas")
        else:
            st.sidebar.success("Login OK")
        


    if button and not(username and password):
        st.warning("Preencha o username e a senha")

    st.markdown("---")


    with st.sidebar.expander("🔗 Links de contato", expanded = False):
        st.link_button("GitHub", "https://github.com/hugogsmendes")
        st.link_button("Linkedin", "https://www.linkedin.com/in/hugogsmendes/")