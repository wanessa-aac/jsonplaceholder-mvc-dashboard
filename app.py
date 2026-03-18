import streamlit as st
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

st.set_page_config(page_title="Dashboard de Comunicação", layout="wide")

st.title("📢 Dashboard de Comunicação Interna")

# -----------------------------
# Função para buscar usuários
# -----------------------------
@st.cache_data(ttl=60)
def buscar_usuarios():
    try:
        response = requests.get(f"{BASE_URL}/users", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("A API demorou mais de 5 segundos para responder.")
    except requests.exceptions.ConnectionError:
        st.error("Erro de conexão com a API.")
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro HTTP: {e}")
    return []

# -----------------------------
# Buscar posts
# -----------------------------
@st.cache_data(ttl=60)
def buscar_posts():
    try:
        response = requests.get(f"{BASE_URL}/posts", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception:
        st.error("Erro ao carregar postagens.")
        return []

# -----------------------------
# Buscar comentários
# -----------------------------
@st.cache_data(ttl=60)
def buscar_comentarios(post_id):
    try:
        response = requests.get(f"{BASE_URL}/posts/{post_id}/comments", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception:
        st.error("Erro ao carregar comentários.")
        return []


usuarios = buscar_usuarios()
posts = buscar_posts()

# -----------------------------
# Sidebar usuários
# -----------------------------
st.sidebar.header("Colaboradores")

usuarios_dict = {u["name"]: u["id"] for u in usuarios}

usuario_selecionado = st.sidebar.selectbox(
    "Selecione um usuário",
    list(usuarios_dict.keys())
)

user_id = usuarios_dict[usuario_selecionado]

st.header(f"Postagens de {usuario_selecionado}")

# -----------------------------
# Filtrar posts por usuário
# -----------------------------
posts_usuario = [p for p in posts if p["userId"] == user_id]

for post in posts_usuario:

    with st.expander(post["title"]):

        st.write(post["body"])

        st.subheader("Comentários")

        comentarios = buscar_comentarios(post["id"])

        for c in comentarios:
            st.markdown(f"**{c['name']}** ({c['email']})")
            st.write(c["body"])
            st.divider()