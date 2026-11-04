# Sistema de Biblioteca

Projeto da disciplina Integração Devops (Ciência da Computação 2026_2) — Prof. Danilo Silva.

Sistema simples de gestão de biblioteca: cadastro de livros (estoque), empréstimo e devolução.

## Stack

- **Backend:** Python (FastAPI)
- **Banco de dados:** MySQL (SQLite em memória nos testes/CI)
- **Testes:** pytest
- **CI/CD:** GitHub Actions
- **Containerização:** Docker / docker-compose
- **Registry:** GitHub Container Registry (GHCR)

## Estrutura do projeto

```
Projeto-devops/
├── app/
│   ├── main.py          # endpoints da API
│   ├── models.py        # modelos (Book, Loan)
│   ├── schemas.py       # validação (Pydantic)
│   ├── crud.py          # regras de negócio
│   └── database.py      # conexão com o banco
├── tests/
│   ├── test_crud.py     # testes unitários
│   └── test_api.py      # testes de integração da API
├── docs/
│   └── ROLLBACK.md      # simulação documentada de rollback
├── .github/workflows/
│   ├── ci.yml           # integração contínua
│   ├── cd.yml           # entrega contínua
│   └── rollback.yml     # rollback manual
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

## Rodando localmente

Nenhuma senha fica no código. O `docker-compose.yml` lê as credenciais de um arquivo `.env`, que não é versionado (está no `.gitignore`). Crie o seu a partir do modelo e defina senhas próprias:

```bash
cp .env.example .env     # no Windows: copy .env.example .env
docker compose up --build
```

A API sobe em `http://localhost:8000` (docs interativas em `/docs`).

| Variável | Uso |
|---|---|
| `MYSQL_DATABASE` | Nome do banco |
| `MYSQL_USER` | Usuário da aplicação |
| `MYSQL_PASSWORD` | Senha do usuário (obrigatória) |
| `MYSQL_ROOT_PASSWORD` | Senha root do MySQL (obrigatória) |

> **Observações:**
> - É necessário ter o **Docker Desktop aberto e rodando** antes de executar o comando acima.
> - Se a porta 3306 já estiver em uso na sua máquina (por um MySQL local instalado fora do Docker), o `docker-compose.yml` expõe o banco na porta 3307 (`3307:3306`) para evitar conflito. A aplicação continua acessando o banco pela rede interna do Docker.
> - Sem a variável `DATABASE_URL`, a aplicação usa SQLite local, o que facilita o desenvolvimento e os testes sem precisar do MySQL.

## Rodando os testes

```bash
pip install -r requirements.txt
pytest -v
```

## Estratégia de branches (Trunk-Based)

- `main`: branch principal, sempre estável e protegida.
- Desenvolvimento em branches curtas a partir da `main`: `feat/nome-da-funcionalidade`, `fix/nome-do-bug`.
- Toda mudança entra via Pull Request para `main`, revisado por outra pessoa do grupo, nunca commit direto.

## Divisão de funções da equipe

| Integrante | Função |
|---|---|
| Fernanda Soares Beleza | Desenvolvedora |
| Rafaela Silva | Qualidade |
| Isabella Santiago | Operações/Infraestrutura |

## Marco 1: Integração Contínua (CI) e Conteinerização Inicial

Para a avaliação do dia 09/09/2026, foi feito:
- Repositório Git estruturado em Trunk-Based, com proteção da branch principal;
- Código-fonte com testes automatizados;
- Pipeline de CI operacional.

## Marco 2: Infraestrutura como Código e Entrega Contínua

Para a avaliação do dia 04/11/2026, foi feito:
- Dockerfile otimizado;
- Orquestração com Docker Compose (aplicação + MySQL);
- Pipeline de CD com publicação no GHCR e deploy automático em homologação;
- Gestão de segredos com GitHub Secrets;
- Versionamento semântico e simulação documentada de rollback.

### Dockerfile
- Build multi-stage: as dependências são instaladas num estágio separado, e a imagem final contém só o necessário.
- Roda com usuário não-root (`appuser`).
- `HEALTHCHECK` consultando `GET /health`.
- `.dockerignore` evita enviar `venv`, testes e arquivos desnecessários ao build.
- O argumento `APP_VERSION` identifica a versão da imagem, exposta em `GET /version`.

### Pipelines (GitHub Actions)

| Workflow | Quando roda | O que faz |
|---|---|---|
| `ci.yml` | Push e Pull Request para `main` | Roda os testes, faz o build da imagem e sobe o compose com o banco (smoke test) |
| `cd.yml` | Criação de uma tag `vX.Y.Z` | Publica a imagem no GHCR e faz o deploy automático em homologação, com smoke test em `/health` e `/version` |
| `rollback.yml` | Manual (Run workflow) | Restaura no ambiente de homologação a imagem da versão informada e valida com smoke test |

### Segredos
No pipeline de CD, as credenciais vêm dos **GitHub Secrets** (`MYSQL_PASSWORD` e `MYSQL_ROOT_PASSWORD`). O login no registry usa o `GITHUB_TOKEN` automático.

### Versionamento semântico e releases
As versões seguem `vMAJOR.MINOR.PATCH`:
- `PATCH`: correção de bug (v1.0.1)
- `MINOR`: funcionalidade nova compatível (v1.1.0)
- `MAJOR`: mudança incompatível (v2.0.0)

Para publicar uma nova versão:
```bash
git checkout main
git pull
git tag v1.0.0
git push origin v1.0.0
```
A imagem fica disponível em `ghcr.io/fernanda031/projeto-devops:1.0.0`. O deploy e o rollback usam sempre a versão explícita, nunca `latest`.

### Rollback
A simulação documentada (versão com falha detectada pelo smoke test e retorno para a versão estável) está em [docs/ROLLBACK.md](docs/ROLLBACK.md).