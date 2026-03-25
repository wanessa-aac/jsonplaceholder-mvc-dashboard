# 📊 JSONPLACEHOLDER-MVC-DASHBOARD

Dashboard de Comunicação Interna para centralizar postagens, comentários e perfis de usuários, construído como protótipo com arquitetura **MVC** consumindo a API pública [JSONPlaceholder](https://jsonplaceholder.typicode.com).

---

## 🚀 Tecnologias

- **Python 3.11+**
- **Streamlit** — interface web interativa
- **Requests** — requisições HTTP à API REST

---

## 🏗️ Arquitetura MVC

O projeto segue o padrão **Model-View-Controller**, separando responsabilidades em três camadas independentes:

```
┌─────────────────────────────────────────────────────┐
│                     USUÁRIO                         │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                   VIEW                              │
│         view/components.py + app.py                 │
│     Componentes Streamlit — exibe os dados          │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                 CONTROLLER                          │
│            controller/controller.py                 │
│     Orquestra chamadas entre Model e View           │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                   MODEL                             │
│    model/api_service.py + model/entities.py         │
│   Requisições HTTP, entidades de domínio            │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│            JSONPlaceholder API                      │
│     /users    /posts    /comments                   │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura do Projeto

```
JSONPLACEHOLDER-MVC-DASHBOARD/
│
├── controller/
│   ├── __init__.py          # Expõe funções do controller
│   └── controller.py        # Orquestra Model e View
│
├── model/
│   ├── __init__.py          # Expõe entidades e serviço
│   ├── api_service.py       # Requisições HTTP + tratamento de erros
│   └── entities.py          # Classes: Usuario, Postagem, Comentario
│
├── view/
│   ├── __init__.py          # Expõe os componentes Streamlit
│   └── components.py        # Componentes visuais da interface
│
├── app.py                   # Ponto de entrada da aplicação
├── requirements.txt          # Dependências do projeto
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Como rodar o projeto localmente

### Pré-requisitos

- Python 3.11 ou superior instalado
- Git instalado

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/wanessa-aac/jsonplaceholder-mvc-dashboard.git
cd JSONPLACEHOLDER-MVC-DASHBOARDj
```

**2. Crie e ative um ambiente virtual**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Execute a aplicação**
```bash
streamlit run app.py
```

**5. Acesse no navegador**
```
http://localhost:8501
```

> ℹ️ A aplicação consome dados diretamente da API pública JSONPlaceholder. É necessário ter conexão com a internet para utilizá-la.

---

## 🔌 Endpoints consumidos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/users` | Lista todos os usuários |
| GET | `/users/{id}` | Retorna um usuário específico |
| GET | `/posts?userId={id}` | Retorna posts de um usuário |
| GET | `/posts/{id}` | Retorna um post específico |
| GET | `/comments?postId={id}` | Retorna comentários de um post |

---

## 🛡️ Tratamento de Falhas

O sistema é resiliente a falhas de rede através das seguintes estratégias:

- **Timeout de 5 segundos** — evita que a aplicação trave aguardando resposta da API
- **Tratamento de HTTP 404** — recurso não encontrado é comunicado ao usuário de forma amigável
- **Tratamento de HTTP 500** — erros internos da API são capturados sem quebrar a aplicação
- **Erro de conexão** — ausência de internet exibe mensagem orientativa ao usuário
- **Resposta inválida** — JSON malformado é capturado antes de causar falhas na interface
- **Exceção customizada `APIError`** — centraliza todas as falhas em um único tipo, facilitando o tratamento na View

---

## 👥 Créditos

Desenvolvido por:

- **Wanessa Costa**
- **Ryan Cassimiro**

Projeto acadêmico — protótipo de Dashboard de Comunicação Interna com arquitetura MVC e integração RESTful.
