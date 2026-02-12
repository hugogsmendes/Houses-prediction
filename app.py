import streamlit as st
import requests

st.set_page_config(page_title = "House Prediction", page_icon = "🤟🏼", layout = "wide")

API_URL = "https://api-houses-prediction.onrender.com"

def register (username: str, password: str):
    url = f"{API_URL}/v1/register"
    try:

        response = requests.post(url, 
                                json = {"username": username, "password": password},
                                headers = {"Content-Type": "application/json",
                                           "accept": "application/json"},
                                timeout = 10)
        
        response.raise_for_status()
        return response.json()
    
    except Exception as err:
        return {"error": str(err)}

def login (username: str, password: str):
    url = f"{API_URL}/v1/login"
    try:

        response = requests.post(url, 
                                data = {"username": username, "password": password},
                                headers = {"Content-Type": "application/x-www-form-urlencoded"},
                                timeout = 10)
        
        response.raise_for_status()
        return response.json()

    except Exception as err:
        return {"error": str(err)}
    
def list_users (tokens: dict):
    url = f"{API_URL}/v1/admin/list"

    try:

        response = requests.get(url,
                                headers = {"Authorization": f"Bearer {tokens['access_token']}"},
                                timeout = 10)
        
        response.raise_for_status()
        return response.json()
    
    except Exception as err:
        return {"error": str(err)}
    
if "tokens" not in st.session_state:
    st.session_state.tokens = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "users" not in st.session_state:
    st.session_state.users =  None


with st.sidebar:

    show_user = st.session_state.current_user or "Faça login"
    st.markdown(f"**User:** {show_user}")

    if st.session_state.tokens and st.session_state.logged_in:
        st.success(f"Você já está logado")
        st.caption("Tokens guardados na sessão.")

        if st.button("Listar usuários"):
            with st.spinner("Buscando os usuários"):
                result = list_users(st.session_state.tokens)
                if "error" in result:
                    st.session_state.users = None
                    st.sidebar.error("Você não tem permissão para usar essa função")
                else:
                    st.session_state.users = result


        if st.button("Logout"):
            st.session_state.tokens = None
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.users = None
            st.rerun()
    else:
        st.title("🔒")
        st.markdown("---")

        username = st.text_input("Username", type = "default", key = "username")
        password = st.text_input("Senha", type = "password")
        button_login = st.button("Login")
        button_register = st.button("Register")
        
        if (button_login or button_register) and not(username and password):
            st.warning("Preencha o username e a senha")

        if button_login and (username and password):
            with st.spinner("Realizando o login"):
                result = login(username, password)

                if "error" in result:
                    st.sidebar.error("Credencias inválidas")
                else:
                    st.sidebar.success("Login OK")
                    st.session_state.tokens = {
                        "access_token": result["access_token"],
                        "refresh_token": result["refresh_token"]
                    }
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.rerun()

        if button_register and (username and password):
            with st.spinner("Criando o usuario"):
                result = register(username, password)

                if "error" in result:
                    st.sidebar.error("Usuario já registrado")
                else:
                    st.sidebar.success("Usuario criado com sucesso")
        
    st.markdown("---")


    with st.sidebar.expander("🔗 Links de contato", expanded = False):
        st.link_button("GitHub", "https://github.com/hugogsmendes")
        st.link_button("Linkedin", "https://www.linkedin.com/in/hugogsmendes/")

if st.session_state.logged_in:

    st.title("🏠 Project Houses Predicition")
    st.subheader("🖩 Inferência do preço de uma casa através de uma API FastAPI")

    if st.session_state.users is not None:
        st.subheader("👥 Usuários")
        if isinstance(st.session_state.users, list):
            st.dataframe(st.session_state.users, width = "stretch")
        else:
            st.json(st.session_state.users)
