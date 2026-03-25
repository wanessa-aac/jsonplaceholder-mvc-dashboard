"""
components.py
-------------
Camada View do Dashboard de Comunicação Interna.
 
Responsável por toda a renderização visual usando Streamlit.
Arquitetura: MVC — este arquivo NÃO faz requisições HTTP
e NÃO contém regras de negócio.
"""
 
import streamlit as st
from model.entities import Usuario, Postagem, Comentario
 
 
def aplicar_estilo():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Serif+Display&display=swap');
 
        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
 
        .dashboard-header {
            background: linear-gradient(135deg, #1a1f2e 0%, #16213e 100%);
            border: 1px solid #2d3561;
            border-radius: 16px;
            padding: 28px 32px;
            margin-bottom: 24px;
        }
        .dashboard-header h1 {
            font-family: 'DM Serif Display', serif;
            font-size: 2rem;
            color: #e8eaf6;
            margin: 0 0 4px 0;
        }
        .dashboard-header p { color: #7986cb; margin: 0; font-size: 0.9rem; }
 
        .user-card {
            background: #1a1f2e;
            border: 1px solid #2d3561;
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 8px;
        }
        .user-card.selected { border-color: #7986cb; background: #1e2540; }
        .user-name { font-weight: 600; color: #e8eaf6; font-size: 0.9rem; }
        .user-meta { color: #7986cb; font-size: 0.78rem; margin-top: 3px; }
        .user-company { color: #5c6bc0; font-size: 0.75rem; margin-top: 2px; }
 
        .avatar {
            display: inline-flex; align-items: center; justify-content: center;
            width: 34px; height: 34px; border-radius: 50%;
            background: linear-gradient(135deg, #3949ab, #5c6bc0);
            color: white; font-weight: 700; font-size: 0.8rem;
            margin-right: 10px; flex-shrink: 0;
        }
 
        .post-card {
            background: #1a1f2e;
            border: 1px solid #2d3561;
            border-left: 3px solid #5c6bc0;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 12px;
        }
        .post-id { font-size: 0.72rem; color: #3949ab; margin-bottom: 4px; }
        .post-title { font-weight: 600; color: #c5cae9; font-size: 0.92rem; text-transform: capitalize; margin-bottom: 6px; }
        .post-body { color: #7986cb; font-size: 0.82rem; line-height: 1.5; text-transform: capitalize; }
 
        .comment-card {
            background: #151929;
            border: 1px solid #252d4a;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 8px;
        }
        .comment-author { font-weight: 600; color: #9fa8da; font-size: 0.82rem; text-transform: capitalize; }
        .comment-email { color: #5c6bc0; font-size: 0.72rem; }
        .comment-body { color: #7986cb; font-size: 0.8rem; margin-top: 6px; line-height: 1.5; text-transform: capitalize; }
 
        .section-title {
            font-family: 'DM Serif Display', serif;
            color: #c5cae9; font-size: 1.2rem;
            margin-bottom: 16px; padding-bottom: 8px;
            border-bottom: 1px solid #2d3561;
        }
 
        .badge {
            background: #3949ab; color: #c5cae9;
            padding: 2px 10px; border-radius: 20px;
            font-size: 0.72rem; font-weight: 600;
        }
 
        .error-box {
            background: #1a0f0f; border: 1px solid #b71c1c;
            border-radius: 10px; padding: 16px 20px;
            color: #ef9a9a; font-size: 0.88rem;
        }
 
        .profile-card {
            background: #1a1f2e; border: 1px solid #2d3561;
            border-radius: 12px; padding: 20px; margin-bottom: 20px;
        }
 
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        .stDeployButton { display: none; }
        [data-testid="stSidebar"] { background: #0d1117; border-right: 1px solid #2d3561; }
    </style>
    """, unsafe_allow_html=True)
 
 
def renderizar_header():
    st.markdown("""
    <div class="dashboard-header">
        <h1>📡 Dashboard de Comunicação Interna</h1>
        <p>Centralizando postagens, comentários e perfis da equipe • JSONPlaceholder API</p>
    </div>
    """, unsafe_allow_html=True)
 
 
def renderizar_erro(mensagem: str):
    st.markdown(f"""
    <div class="error-box">
        ⚠️ <strong>Falha na comunicação com a API</strong><br>{mensagem}
    </div>
    """, unsafe_allow_html=True)
 
 
def renderizar_card_usuario(usuario: Usuario, selecionado: bool = False):
    iniciais = "".join([p[0].upper() for p in usuario.nome.split()[:2]])
    classe = "user-card selected" if selecionado else "user-card"
    empresa = usuario.empresa.nome if usuario.empresa else "—"
    st.markdown(f"""
    <div class="{classe}">
        <div style="display:flex;align-items:center;">
            <div class="avatar">{iniciais}</div>
            <div>
                <div class="user-name">{usuario.nome}</div>
                <div class="user-meta">@{usuario.usuario} · {usuario.email}</div>
                <div class="user-company">🏢 {empresa}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
 
def renderizar_perfil_usuario(usuario: Usuario):
    iniciais = "".join([p[0].upper() for p in usuario.nome.split()[:2]])
    empresa = usuario.empresa.nome if usuario.empresa else "—"
    slogan = usuario.empresa.slogan if usuario.empresa else "—"
    cidade = usuario.endereco.cidade if usuario.endereco else "—"
    st.markdown(f"""
    <div class="profile-card">
        <div style="display:flex;align-items:center;margin-bottom:16px;">
            <div class="avatar" style="width:48px;height:48px;font-size:1.1rem;">{iniciais}</div>
            <div>
                <div style="font-weight:600;color:#e8eaf6;font-size:1.05rem;">{usuario.nome}</div>
                <div style="color:#7986cb;font-size:0.82rem;">@{usuario.usuario}</div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:0.82rem;">
            <div><span style="color:#5c6bc0;">📧</span> <span style="color:#c5cae9;">{usuario.email}</span></div>
            <div><span style="color:#5c6bc0;">📞</span> <span style="color:#c5cae9;">{usuario.telefone}</span></div>
            <div><span style="color:#5c6bc0;">🏢</span> <span style="color:#c5cae9;">{empresa}</span></div>
            <div><span style="color:#5c6bc0;">📍</span> <span style="color:#c5cae9;">{cidade}</span></div>
        </div>
        <div style="margin-top:10px;color:#4a5568;font-size:0.78rem;font-style:italic;">"{slogan}"</div>
    </div>
    """, unsafe_allow_html=True)
 
 
def renderizar_postagem(postagem: Postagem, autor_nome: str = ""):
    autor_info = f"<span style='color:#5c6bc0;font-size:0.75rem;'>por {autor_nome}</span>" if autor_nome else ""
    st.markdown(f"""
    <div class="post-card">
        <div class="post-id">#{postagem.id} {autor_info}</div>
        <div class="post-title">{postagem.titulo}</div>
        <div class="post-body">{postagem.corpo}</div>
    </div>
    """, unsafe_allow_html=True)
 
 
def renderizar_comentario(comentario: Comentario):
    st.markdown(f"""
    <div class="comment-card">
        <div class="comment-author">{comentario.nome}</div>
        <div class="comment-email">{comentario.email}</div>
        <div class="comment-body">{comentario.corpo}</div>
    </div>
    """, unsafe_allow_html=True)