import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

st.set_page_config(page_title = "House Prediction", page_icon = "🤟🏼", layout = "wide")

API_URL = st.secrets["API_URL"]


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
    
@st.cache_data(ttl = 30)   
def list_users (access_token: str):
    url = f"{API_URL}/v1/admin/list"

    try:

        response = requests.get(url,
                                headers = {"Authorization": f"Bearer {access_token}"},
                                timeout = 10)
        
        response.raise_for_status()
        return response.json()
    
    except Exception as err:
        return {"error": str(err)}
    
def delete_user (username: str, tokens: dict):
    url = f"{API_URL}/v1/admin/delete"

    try:

        response = requests.delete(url,
                                json = {"username": username},
                                headers = {"Authorization": f"Bearer {tokens['access_token']}"},
                                timeout = 10)
        response.raise_for_status()
        return response.json()
    
    except Exception as err:
        return {"error": str(err)}

st.cache_data(ttl = 30)
def get_df (access_token: str):

    url = f"{API_URL}/v1/model/df"

    try:

        response = requests.get(url,
                                headers = {"Authorization": f"Bearer {access_token}"},
                                timeout = 10)
        response.raise_for_status()
        return response.content
    
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
                result = list_users(st.session_state.tokens["access_token"])
                if "error" in result:
                    st.session_state.users = None
                    st.sidebar.error("Você não tem permissão para usar essa função")
                else:
                    st.session_state.users = result

        csv_bytes = get_df(st.session_state.tokens["access_token"])
        try:
            st.download_button("Download Dataset",
                              data = csv_bytes,
                              file_name = "dataset.csv",
                              mime = "text/csv")
        except Exception:
            st.sidebar.error("Não foi possível baixar o dataset no momento")

        if st.button("Logout"):
            list_users.clear()
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
        button_back = st.button("Voltar")

        if button_back:
            st.session_state.users = None
            st.rerun()

        users = st.session_state.users if isinstance(st.session_state.users, list) else []
            # Cabeçalho
        h1, h2 = st.columns([6, 1])
        h1.markdown("**Usuário**")
        h2.markdown("**Ações**")

        st.markdown("---")

        for u in users:
        # tenta suportar lista de dicts ou lista de strings
            username = u.get("username") if isinstance(u, dict) else str(u)

            c1, c2 = st.columns([6, 1])
            c1.write(username)

            # Opção 1 (sempre funciona): emoji
            if c2.button("🗑️", key=f"del_{username}", help=f"Deletar {username}"):
            # confirmação simples
                st.session_state["confirm_delete"] = username

        # Confirmação fora do loop (evita múltiplos botões conflitando)
        if st.session_state.get("confirm_delete"):
            target = st.session_state["confirm_delete"]
            st.warning(f"Confirmar exclusão do usuário **{target}**?")

            b1, b2 = st.columns([1, 1])
            if b1.button("Confirmar", key="confirm_del_btn"):

                result = delete_user(target, st.session_state.tokens)

                if "error" in result:
                    st.error("Você não tem permissão para usar essa função")
                else:
                    st.success("Usuário deletado")
                    list_users.clear()
                    st.session_state["confirm_delete"] = None
                    st.session_state.users = None
                    st.rerun()

            if b2.button("Cancelar", key="cancel_del_btn"):
                st.session_state["confirm_delete"] = None
                st.rerun()
    

