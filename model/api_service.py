"""
api_model.py
------------
Camada Model do Dashboard de Comunicação Interna.
Responsável por toda comunicação com a API JSONPlaceholder.

Arquitetura: MVC — este arquivo é exclusivamente o Model.
Nenhuma lógica de interface ou apresentação deve residir aqui.
"""

import requests

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------

BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 5  # segundos


# ---------------------------------------------------------------------------
# Exceção customizada
# ---------------------------------------------------------------------------

class APIError(Exception):
    """
    Sinaliza qualquer falha na comunicação com a API.

    Atributos:
        message  -- descrição legível do erro
        status_code -- código HTTP retornado (None se não houve resposta)
    """

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        if self.status_code:
            return f"[HTTP {self.status_code}] {self.message}"
        return self.message


# ---------------------------------------------------------------------------
# Função auxiliar privada — único ponto de contato com a rede
# ---------------------------------------------------------------------------

def _get(endpoint: str) -> dict | list:
    """
    Executa uma requisição GET para o endpoint informado.

    Centraliza:
    - Montagem da URL completa
    - Aplicação do timeout
    - Tratamento de todos os erros de rede e HTTP

    Retorna o JSON deserializado (dict ou list).
    Lança APIError em qualquer situação de falha.
    """
    url = f"{BASE_URL}{endpoint}"

    try:
        response = requests.get(url, timeout=TIMEOUT)

        # Lança HTTPError para códigos 4xx e 5xx
        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        raise APIError(
            f"A API não respondeu em {TIMEOUT} segundos. Tente novamente mais tarde."
        )

    except requests.exceptions.ConnectionError:
        raise APIError(
            "Não foi possível conectar à API. Verifique sua conexão com a internet."
        )

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else None

        if status == 404:
            raise APIError("Recurso não encontrado na API (404).", status_code=404)
        elif status == 500:
            raise APIError("Erro interno no servidor da API (500).", status_code=500)
        else:
            raise APIError(f"Erro HTTP inesperado: {e}", status_code=status)

    except requests.exceptions.JSONDecodeError:
        raise APIError("A API retornou uma resposta inválida (não é JSON).")

    except requests.exceptions.RequestException as e:
        # Captura genérica para qualquer outro erro da biblioteca requests
        raise APIError(f"Erro inesperado na requisição: {e}")


# ---------------------------------------------------------------------------
# Funções públicas — Users
# ---------------------------------------------------------------------------

def get_users() -> list[dict]:
    """
    Retorna a lista completa de usuários.

    Exemplo de retorno:
        [
            {"id": 1, "name": "Leanne Graham", "email": "...", ...},
            ...
        ]
    """
    return _get("/users")


def get_user(user_id: int) -> dict:
    """
    Retorna os dados de um único usuário pelo ID.

    Parâmetros:
        user_id -- ID do usuário (inteiro positivo)

    Exemplo de retorno:
        {"id": 1, "name": "Leanne Graham", "username": "Bret", "email": "...", ...}
    """
    return _get(f"/users/{user_id}")


# ---------------------------------------------------------------------------
# Funções públicas — Posts
# ---------------------------------------------------------------------------

def get_posts(user_id: int | None = None) -> list[dict]:
    """
    Retorna posts. Se user_id for informado, filtra pelo usuário.

    Parâmetros:
        user_id -- (opcional) filtra posts de um usuário específico

    Exemplo de retorno:
        [
            {"id": 1, "userId": 1, "title": "...", "body": "..."},
            ...
        ]
    """
    if user_id is not None:
        return _get(f"/posts?userId={user_id}")
    return _get("/posts")


def get_post(post_id: int) -> dict:
    """
    Retorna os dados de um único post pelo ID.

    Parâmetros:
        post_id -- ID do post (inteiro positivo)

    Exemplo de retorno:
        {"id": 1, "userId": 1, "title": "...", "body": "..."}
    """
    return _get(f"/posts/{post_id}")


# ---------------------------------------------------------------------------
# Funções públicas — Comments
# ---------------------------------------------------------------------------

def get_comments(post_id: int) -> list[dict]:
    """
    Retorna todos os comentários de um post específico.

    Parâmetros:
        post_id -- ID do post pai

    Exemplo de retorno:
        [
            {"id": 1, "postId": 1, "name": "...", "email": "...", "body": "..."},
            ...
        ]
    """
    return _get(f"/comments?postId={post_id}")