"""
app.py
------
Ponto de entrada do Dashboard de Comunicação Interna.
Arquitetura: MVC — chama apenas o Controller, nunca a API diretamente.
"""

import streamlit as st
from controller.controller import (
    carregar_usuarios,
    carregar_usuario_completo,
    carregar_postagens_do_usuario,
    carregar_postagem_completa,
    APIError,
)
from view.components import (
    aplicar_estilo,
    renderizar_header,
    renderizar_erro,
    renderizar_card_usuario,
    renderizar_perfil_usuario,
    renderizar_postagem,
    renderizar_comentario,
)

# ─── Configuração ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard de Comunicação Interna",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_estilo()

# ─── Estado da sessão ─────────────────────────────────────────────────────────
if "usuario_id" not in st.session_state:
    st.session_state.usuario_id = None
if "postagem_id" not in st.session_state:
    st.session_state.postagem_id = None

# ─── Cache ────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60, show_spinner=False)
def obter_usuarios():
    return carregar_usuarios()

@st.cache_data(ttl=60, show_spinner=False)
def obter_usuario_completo(uid: int):
    return carregar_usuario_completo(uid)

@st.cache_data(ttl=60, show_spinner=False)
def obter_postagens_usuario(uid: int):
    return carregar_postagens_do_usuario(uid)

@st.cache_data(ttl=60, show_spinner=False)
def obter_postagem_completa(pid: int):
    return carregar_postagem_completa(pid)

# ─── Carregamento inicial ─────────────────────────────────────────────────────
usuarios = []
erro_usuarios = None

try:
    with st.spinner("Carregando colaboradores..."):
        usuarios = obter_usuarios()
except APIError as e:
    erro_usuarios = str(e)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='section-title'>👥 Colaboradores</div>", unsafe_allow_html=True)

    if erro_usuarios:
        renderizar_erro(erro_usuarios)
    else:
        nomes = ["Todos os colaboradores"] + [u.nome for u in usuarios]
        escolha = st.selectbox("Colaborador", nomes, label_visibility="collapsed")

        filtrados = usuarios if escolha == "Todos os colaboradores" else [u for u in usuarios if u.nome == escolha]

        st.markdown(f"<span class='badge'>{len(filtrados)} colaboradores</span><br><br>", unsafe_allow_html=True)

        for usuario in filtrados:
            selecionado = st.session_state.usuario_id == usuario.id
            renderizar_card_usuario(usuario, selecionado)

            if st.button("Ver postagens", key=f"ps_{usuario.id}", use_container_width=True):
                st.session_state.usuario_id = usuario.id
                st.session_state.postagem_id = None
                st.rerun()

            # Perfil expandido na sidebar quando selecionado
            if selecionado:
                cidade = usuario.endereco.cidade if usuario.endereco else "—"
                empresa = usuario.empresa.nome if usuario.empresa else "—"
                slogan = usuario.empresa.slogan if usuario.empresa else "—"
                st.markdown(f"""
                <div style="font-size:0.78rem;color:#7986cb;padding:10px 4px 4px 4px;
                            border-top:1px solid #2d3561;margin-top:4px;line-height:1.8;">
                    📍 {cidade}<br>
                    🏢 {empresa}<br>
                    📞 {usuario.telefone}<br>
                    📧 {usuario.email}<br>
                    <span style="color:#4a5568;font-style:italic;font-size:0.72rem;">"{slogan}"</span>
                </div>
                """, unsafe_allow_html=True)

        # Botão para voltar ao feed geral
        if st.session_state.usuario_id:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("← Voltar ao feed geral", use_container_width=True):
                st.session_state.usuario_id = None
                st.session_state.postagem_id = None
                st.rerun()

# ─── Área principal ───────────────────────────────────────────────────────────
renderizar_header()

uid = st.session_state.usuario_id
pid = st.session_state.postagem_id

# ── Modo: colaborador selecionado ─────────────────────────────────────────────
if uid:
    try:
        with st.spinner("Carregando colaborador..."):
            usuario = obter_usuario_completo(uid)
            postagens_u = obter_postagens_usuario(uid)

        renderizar_perfil_usuario(usuario)
        st.markdown(
            f"<div class='section-title'>Postagens de {usuario.nome} "
            f"<span class='badge'>{len(postagens_u)} postagens</span></div>",
            unsafe_allow_html=True
        )

        for postagem in postagens_u:
            renderizar_postagem(postagem)

            # Botão ver comentários
            if st.button("💬 Ver comentários", key=f"uc_{postagem.id}"):
                if st.session_state.postagem_id == postagem.id:
                    # Toggle: clicou de novo, fecha
                    st.session_state.postagem_id = None
                else:
                    st.session_state.postagem_id = postagem.id
                st.rerun()

            # Comentários inline abaixo da postagem
            if pid == postagem.id:
                try:
                    with st.spinner("Carregando comentários..."):
                        post_completa = obter_postagem_completa(pid)

                    st.markdown(
                        f"<div style='padding-left:16px;border-left:2px solid #2d3561;margin:8px 0 16px 0;'>"
                        f"<span class='badge'>{post_completa.total_comentarios} comentários</span><br><br>",
                        unsafe_allow_html=True
                    )
                    for comentario in post_completa.comentarios:
                        renderizar_comentario(comentario)
                    st.markdown("</div>", unsafe_allow_html=True)

                except APIError as e:
                    renderizar_erro(str(e))

    except APIError as e:
        renderizar_erro(str(e))

# ── Modo: feed geral ──────────────────────────────────────────────────────────
else:
    st.markdown("<div class='section-title'>📰 Feed Geral</div>", unsafe_allow_html=True)
    try:
        with st.spinner("Carregando feed..."):
            from model.api_service import get_posts
            from model.entities import Postagem
            postagens = [Postagem.from_dict(p) for p in get_posts()]

        mapa = {u.id: u for u in usuarios}
        st.markdown(f"<span class='badge'>{len(postagens)} postagens</span><br><br>", unsafe_allow_html=True)

        for postagem in postagens:
            autor = mapa.get(postagem.user_id)
            renderizar_postagem(postagem, autor.nome if autor else f"Usuário #{postagem.user_id}")

            if st.button("💬 Ver comentários", key=f"fc_{postagem.id}"):
                if st.session_state.postagem_id == postagem.id:
                    st.session_state.postagem_id = None
                else:
                    st.session_state.postagem_id = postagem.id
                st.rerun()

            # Comentários inline abaixo da postagem
            if pid == postagem.id:
                try:
                    with st.spinner("Carregando comentários..."):
                        post_completa = obter_postagem_completa(pid)

                    st.markdown(
                        f"<div style='padding-left:16px;border-left:2px solid #2d3561;margin:8px 0 16px 0;'>"
                        f"<span class='badge'>{post_completa.total_comentarios} comentários</span><br><br>",
                        unsafe_allow_html=True
                    )
                    for comentario in post_completa.comentarios:
                        renderizar_comentario(comentario)
                    st.markdown("</div>", unsafe_allow_html=True)

                except APIError as e:
                    renderizar_erro(str(e))

    except APIError as e:
        renderizar_erro(str(e))