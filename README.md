# CRUD em Django - A3 Unisul
# Resumo
Gerenciamento de Estoque - Projeto Django

Este projeto é um sistema de gerenciamento de estoque desenvolvido com Django e MySQL. O sistema permite o controle de produtos, movimentação de estoque (entradas e saídas), categorias de produtos e muito mais. Além disso, é possível realizar o cadastro, edição, e exclusão de produtos e categorias, tudo a partir de uma interface amigável e responsiva.

**O sistema possui as seguintes funcionalidades:**

  - Cadastro, edição e exclusão de produtos.

  - Cadastro de novas categorias e edição das mesmas.

  - Movimentação de produtos no estoque (entradas e saídas).

  - Alerta de produtos com estoque baixo.

  - Relatórios de produtos ativos e inativos.

  - Interface amigável utilizando Bootstrap.

### Instruções de Instalação

Requisitos

  - Python 3.8+

  - MySQL

  - Git

**Passos para Instalação**

  Clone o repositório:

         git clone <URL_DO_REPOSITORIO>
          cd <NOME_DO_PROJETO>

Crie e ative um ambiente virtual:

  - No Linux/Mac:

        python3 -m venv venv
        source venv/bin/activate.ps1

No Windows:

      python -m venv venv
      venv\Scripts\activate

**Instale as dependências do projeto:**

    pip install -r requirements.txt

**Configurar o banco de dados:**

Crie um banco de dados no MySQL:

    CREATE DATABASE gerenciamento_estoque;

Atualize as configurações do banco de dados no arquivo settings.py do Django:

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gerenciamento_estoque',
        'USER': '<SEU_USUARIO>',
        'PASSWORD': '<SUA_SENHA>',
        'HOST': 'localhost',
        'PORT': '3306',
    }
    }

Execute as migrações:

    python manage.py makemigrations
    python manage.py migrate

Crie um superusuário para acessar o admin do Django:

    python manage.py createsuperuser

Siga as instruções para definir um nome de usuário, e-mail e senha.

**Inicie o servidor:**

    python manage.py runserver

O servidor será iniciado e o sistema poderá ser acessado em http://127.0.0.1:8000/.

Acesse a interface de administração do Django (opcional):

Acesse http://127.0.0.1:8000/admin/ e faça login com o superusuário criado.

  - Considerações

Certifique-se de que o servidor MySQL está rodando antes de iniciar o projeto.

Todas as dependências necessárias estão listadas no arquivo requirements.txt.

  ### Funcionalidades Futuras

- A proxima grande funcionalidade para ser implementada vai ser a autenticação de usuarios, cada pessoa que for utilizar o sistema poderá cadastrar seu próprio usuario.

- Melhorar a interface para gerenciamento de movimentações de estoque.

- Implementar relatórios mais detalhados com visualizações gráficas.

Se precisar de ajuda ou tiver sugestões, fique à vontade para abrir uma issue no repositório. Espero que você goste do projeto!

