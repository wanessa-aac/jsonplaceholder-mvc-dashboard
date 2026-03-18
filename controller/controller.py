"""
controller.py
-------------
Camada Controller do Dashboard de Comunicação Interna.

Responsável por orquestrar o fluxo de dados entre o Model e a View:
  - Chama as funções do api_service.py para buscar dados brutos da API
  - Converte os dicts retornados nas entidades definidas em entities.py
  - Devolve objetos prontos para a View consumir, sem expor detalhes da API

Arquitetura: MVC — este arquivo NÃO faz requisições HTTP diretamente
e NÃO contém lógica de interface Streamlit.
"""

from model.api_service import (
    get_users,
    get_user,
    get_posts,
    get_post,
    get_comments,
    APIError,
)
from model.entities import Usuario, Postagem, Comentario


# ---------------------------------------------------------------------------
# Re-exporta APIError para que a View só precise importar do controller
# ---------------------------------------------------------------------------

__all__ = ["APIError", "carregar_usuarios", "carregar_usuario_completo",
           "carregar_postagens_do_usuario", "carregar_postagem_completa"]


# ---------------------------------------------------------------------------
# Funções públicas do Controller
# ---------------------------------------------------------------------------

def carregar_usuarios() -> list[Usuario]:
    """
    Retorna a lista completa de usuários como objetos Usuario.

    Lança APIError se a comunicação com a API falhar.

    Exemplo de uso na View:
        try:
            usuarios = carregar_usuarios()
        except APIError as e:
            st.error(e.message)
    """
    dados = get_users()
    return [Usuario.from_dict(u) for u in dados]


def carregar_usuario_completo(user_id: int) -> Usuario:
    """
    Retorna um Usuario com suas postagens já populadas.
    Cada postagem ainda não carrega comentários (lazy — sob demanda).

    Parâmetros:
        user_id -- ID do usuário a ser carregado

    Lança APIError se a comunicação com a API falhar.

    Exemplo de uso na View:
        try:
            usuario = carregar_usuario_completo(1)
            st.write(usuario.nome)
            st.write(f"{usuario.total_postagens} postagens")
        except APIError as e:
            st.error(e.message)
    """
    dados_usuario = get_user(user_id)
    usuario = Usuario.from_dict(dados_usuario)

    dados_postagens = get_posts(user_id=user_id)
    usuario.adicionar_postagens(dados_postagens)

    return usuario


def carregar_postagens_do_usuario(user_id: int) -> list[Postagem]:
    """
    Retorna apenas a lista de postagens de um usuário,
    sem carregar os dados completos do perfil.

    Útil para listagens rápidas onde o perfil já foi carregado antes.

    Parâmetros:
        user_id -- ID do usuário dono das postagens

    Lança APIError se a comunicação com a API falhar.
    """
    dados = get_posts(user_id=user_id)
    return [Postagem.from_dict(p) for p in dados]


def carregar_postagem_completa(post_id: int) -> Postagem:
    """
    Retorna uma Postagem com seus comentários já populados.

    Parâmetros:
        post_id -- ID da postagem a ser carregada

    Lança APIError se a comunicação com a API falhar.

    Exemplo de uso na View:
        try:
            postagem = carregar_postagem_completa(1)
            st.write(postagem.titulo)
            for comentario in postagem.comentarios:
                st.write(comentario.corpo)
        except APIError as e:
            st.error(e.message)
    """
    dados_post = get_post(post_id)
    postagem = Postagem.from_dict(dados_post)

    dados_comentarios = get_comments(post_id=post_id)
    postagem.adicionar_comentarios(dados_comentarios)

    return postagem