"""
entities.py
-----------
Camada Model — Classes de domínio do Dashboard de Comunicação Interna.

Representa as entidades do negócio mapeadas a partir do JSON
retornado pela API JSONPlaceholder.

Arquitetura: MVC — este arquivo é exclusivamente o Model.
Nenhuma lógica de interface ou requisição HTTP deve residir aqui.
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Entidades de suporte (objetos aninhados no JSON de Usuario)
# ---------------------------------------------------------------------------

@dataclass
class Endereco:
    """
    Representa o endereço físico de um usuário.
    Mapeado a partir do objeto 'address' no JSON de /users.
    """
    rua: str
    cidade: str
    cep: str

    @classmethod
    def from_dict(cls, data: dict) -> "Endereco":
        return cls(
            rua=data.get("street", ""),
            cidade=data.get("city", ""),
            cep=data.get("zipcode", ""),
        )


@dataclass
class Empresa:
    """
    Representa a empresa associada a um usuário.
    Mapeado a partir do objeto 'company' no JSON de /users.
    """
    nome: str
    slogan: str

    @classmethod
    def from_dict(cls, data: dict) -> "Empresa":
        return cls(
            nome=data.get("name", ""),
            slogan=data.get("catchPhrase", ""),
        )


# ---------------------------------------------------------------------------
# Entidades principais
# ---------------------------------------------------------------------------

@dataclass
class Comentario:
    """
    Representa um comentário feito em uma postagem.
    Mapeado a partir do JSON de /comments.

    Relação: N comentários pertencem a 1 Postagem (N:1).
    """
    id: int
    post_id: int
    nome: str
    email: str
    corpo: str

    @classmethod
    def from_dict(cls, data: dict) -> "Comentario":
        return cls(
            id=data.get("id", 0),
            post_id=data.get("postId", 0),
            nome=data.get("name", ""),
            email=data.get("email", ""),
            corpo=data.get("body", ""),
        )


@dataclass
class Postagem:
    """
    Representa uma postagem feita por um usuário.
    Mapeado a partir do JSON de /posts.

    Relações:
        - N postagens pertencem a 1 Usuario (N:1)
        - 1 postagem possui N Comentarios (1:N)
    """
    id: int
    user_id: int
    titulo: str
    corpo: str
    comentarios: list[Comentario] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Postagem":
        return cls(
            id=data.get("id", 0),
            user_id=data.get("userId", 0),
            titulo=data.get("title", ""),
            corpo=data.get("body", ""),
        )

    def adicionar_comentarios(self, lista: list[dict]) -> None:
        """Popula a lista de comentários a partir de uma lista de dicts da API."""
        self.comentarios = [Comentario.from_dict(c) for c in lista]

    @property
    def total_comentarios(self) -> int:
        """Retorna a quantidade de comentários carregados nesta postagem."""
        return len(self.comentarios)


@dataclass
class Usuario:
    """
    Representa um usuário/funcionário da empresa.
    Mapeado a partir do JSON de /users.

    Relação: 1 usuário possui N Postagens (1:N).
    """
    id: int
    nome: str
    usuario: str
    email: str
    telefone: str
    website: str
    endereco: Endereco | None
    empresa: Empresa | None
    postagens: list[Postagem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        endereco = Endereco.from_dict(data["address"]) if "address" in data else None
        empresa = Empresa.from_dict(data["company"]) if "company" in data else None

        return cls(
            id=data.get("id", 0),
            nome=data.get("name", ""),
            usuario=data.get("username", ""),
            email=data.get("email", ""),
            telefone=data.get("phone", ""),
            website=data.get("website", ""),
            endereco=endereco,
            empresa=empresa,
        )

    def adicionar_postagens(self, lista: list[dict]) -> None:
        """Popula a lista de postagens a partir de uma lista de dicts da API."""
        self.postagens = [Postagem.from_dict(p) for p in lista]

    @property
    def total_postagens(self) -> int:
        """Retorna a quantidade de postagens carregadas para este usuário."""
        return len(self.postagens)