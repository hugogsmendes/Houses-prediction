import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import io

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
    
@st.cache_data(ttl = 30, show_spinner = False)   
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

st.cache_data(ttl = 30, show_spinner = False)
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

def predict(access_token: str, payload: dict):

    url = f"{API_URL}/v1/model/predict"

    try:

        response = requests.post(url,
                                 json = payload,
                                 headers = {"Authorization": f"Bearer {access_token}"},
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
if "csv_bytes" not in st.session_state:
    st.session_state.csv_bytes = None
if "df" not in st.session_state:
    st.session_state.df = None


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
                    st.session_state.df = None
                    st.session_state.users = result
        try:
            st.download_button("Download Dataset",
                              data = st.session_state.csv_bytes,
                              file_name = "dataset.csv",
                              mime = "text/csv")
        except Exception:
            st.sidebar.error("Não foi possível baixar o dataset no momento")

        if st.button("Exibir Dataframe"):
            df = pd.read_csv(io.BytesIO(st.session_state.csv_bytes), sep = ",")
            st.session_state.users = None
            st.session_state.df = df


        if st.button("Logout"):
            list_users.clear()
            st.session_state.tokens = None
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.users = None
            st.session_state.csv_bytes = None
            st.session_state.df = None
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
                    st.session_state.csv_bytes = get_df(st.session_state.tokens["access_token"])
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

    if st.session_state.users is None and st.session_state.df is None:

        with st.form("predict_form", clear_on_submit=False):
            st.subheader("🔮 Previsão")
            c1, c2, c3 = st.columns(3)

            with c1:
                area = st.number_input("Area", min_value=0, step=1, value=200)
                quartos = st.number_input("Quartos", min_value=0, step=1, value=2)
                banheiros = st.number_input("Banheiros", min_value=0, step=1, value=1)
                andares = st.number_input("Andares", min_value=0, step=1, value=1)

            with c2:
                acesso_rodovia = st.selectbox("Acesso à rodovia (0/1)", [0, 1], index=0)
                quarto_hospede = st.selectbox("Quarto hóspede (0/1)", [0, 1], index=0)
                porao = st.selectbox("Porão (0/1)", [0, 1], index=0)
                aquecimento_agua = st.selectbox("Aquecimento de água (0/1)", [0, 1], index=0)

            with c3:
                ar_condicionado = st.selectbox("Ar condicionado (0/1)", [0, 1], index=0)
                vagas_estacionamento = st.number_input("Vagas de estacionamento", min_value=0, step=1, value=1)
                area_preferencial = st.selectbox("Área preferencial (0/1)", [0, 1], index=0)
                status_mobilia_sem_mobilia = st.selectbox("Status mobília: sem mobília (0/1)", [0, 1], index=1)
                status_mobilia_semi_mobiliada = st.selectbox("Status mobília: semi mobiliada (0/1)", [0, 1], index=0)


            submitted = st.form_submit_button("Prever")

        if submitted:
            payload = {
                "area": int(area),
                "quartos": int(quartos),
                "banheiros": int(banheiros),
                "andares": int(andares),
                "acesso_rodovia": int(acesso_rodovia),
                "quarto_hospede": int(quarto_hospede),
                "porao": int(porao),
                "aquecimento_agua": int(aquecimento_agua),
                "ar_condicionado": int(ar_condicionado),
                "vagas_estacionamento": int(vagas_estacionamento),
                "area_preferencial": int(area_preferencial),
                "status_mobilia_sem_mobilia": int(status_mobilia_sem_mobilia),
                "status_mobilia_semi_mobiliada": int(status_mobilia_semi_mobiliada),
            }
            result = predict(st.session_state.tokens["access_token"], payload)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"Preço previsto: {result["preco_previsto"]}")


    if st.session_state.df is not None:
        st.dataframe(st.session_state.df)

        button_back = st.button("Voltar")

        if button_back:
            st.session_state.df = None
            st.rerun()

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
    

