## 🚗 Sobre o Projeto

O **ParkHub** é uma plataforma projetada para modernizar a gestão de estacionamentos. Ele atua como um hub central, conectando motoristas que procuram vagas com gestores que precisam de ferramentas eficientes para administrar seus negócios.

Este repositório contém a API backend do sistema.

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes tecnologias:

- **Backend:** Python (com FastAPI, Pydantic, SQLAlchemy)
- **Banco de Dados:** PostgreSQL
- **Blob Storage:** AWS S3 (LocalStack para uso local)
- **Migrations:** Alembic
- **Containerização:** Docker & Docker Compose
- **Gerenciador de BD (GUI):** PgAdmin

---

## 🚀 Começando

Siga estas instruções para ter o projeto rodando em seu ambiente local para desenvolvimento e testes.

### Pré-requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/official-parkhub/park-hub](https://github.com/official-parkhub/park-hub)
    cd parkhub
    ```

2.  **Configure as Variáveis de Ambiente:**
    Copie o arquivo de exemplo `.env.example` para um novo arquivo `.env` na pasta `env/`.

    ```bash
    cp env/.env.example env/.env
    ```

    Em seguida, abra o arquivo `env/.env` e altere as variáveis conforme sua necessidade.

    ```ini
    # API variables
    API_VERSION=0.0.1
    API_HOST=0.0.0.0
    API_PORT=8080
    API_RELOAD=true

    # Auth variables
    AUTH_SECRET_KEY=secret
    AUTH_REFRESH_SECRET_KEY=refresh_secret

    # Postgres variables
    POSTGRES_USER=parkhub
    POSTGRES_PASSWORD=password
    POSTGRES_DATABASE=postgres
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432

    # PgAdmin variables
    PGADMIN_DEFAULT_EMAIL=admin@parkhub.com
    PGADMIN_DEFAULT_PASSWORD=admin
    ```

3.  **Suba os Containers:**
    Use o Docker Compose para construir e iniciar todos os serviços em modo "detached" (-d).

    ```bash
    docker compose up -d
    ```

4. **Rode as migrations**
    ```bash
    sudo docker compose run --rm api alembic upgrade head
    ```

5.  **Pronto!** A aplicação estará rodando:
    - A API estará acessível em `http://localhost:8080`.
    - O PgAdmin estará acessível em `http://localhost:5050`.

---

### Instalação do pre-commit

Este projeto utiliza o `pre-commit` para garantir a formatação do código antes de cada commit. Para instalá-lo e configurá-lo no repositório, execute:

```bash
uvx pre-commit install
```

### Instalação Local com Ambiente Virtual

Para melhorar a experiência de desenvolvimento, especialmente no uso de IntelliSense na IDE, é recomendável instalar as dependências localmente:

1. Sincronize as dependências:
   ```bash
   uv sync
   ```

2. Ative o ambiente virtual:
   ```bash
   source .venv/bin/activate
   ```

3. Configure o ambiente virtual na sua IDE. No caso do VSCode:
   - Abra a Command Palette (Ctrl+Shift+P).
   - Pesquise por **Python: Select Interpreter**.
   - Escolha **Enter Interpreter Path** e insira `.venv/bin/python`.

### Desenvolvimento com Docker

Para configurar e executar a aplicação dentro de containers Docker:

1. Construa e inicie os containers:
   ```bash
   docker compose up -d
   ```

## Banco de Dados

A aplicação utiliza PostgreSQL como banco de dados. A execução do banco é feita preferencialmente via Docker Compose.

### Inicializando o Banco de Dados

Para iniciar o banco de dados:
```bash
docker compose up -d postgres
```

Caso seja a primeira execução ou você precise limpar todos os dados:
```bash
sudo rm -rf .tmp/volumes/pg/
sudo docker compose up -d --force-recreate postgres
sleep 2s
sudo docker compose run --rm api alembic upgrade head
```

## 🗄️ Migrations com Alembic

Para gerenciar as alterações no schema do banco de dados, utilizamos o Alembic.

### Gerando uma Nova Migration

Após fazer alterações nas models do projeto (em `*/models/`), gere um novo arquivo de migration com o seguinte comando. Lembre-se de que os containers do Docker precisam estar de pé.

```bash
docker compose run --rm api alembic revision --autogenerate -m "Sua mensagem descritiva aqui"
```

### Aplicando Migrations

Para aplicar todas as migrations pendentes ao banco de dados e atualizar o schema para a versão mais recente, execute:

```bash
docker compose run --rm api alembic upgrade head
```

### Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
