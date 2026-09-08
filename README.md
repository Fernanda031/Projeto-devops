# Sistema de Biblioteca

Projeto da disciplina Integração Devops (Ciência da Computação 2026) — Prof. Danilo Silva.

Sistema simples de gestão de biblioteca: cadastro de livros (estoque), empréstimo e devolução.

## Stack

- **Backend:** Python (FastAPI)
- **Banco de dados:** MySQL (SQLite em memória nos testes/CI)
- **Testes:** pytest
- **CI:** GitHub Actions
- **Containerização:** Docker / docker-compose

## Estrutura do projeto

```
library-system/
├── app/
│   ├── main.py        
│   ├── models.py      
│   ├── schemas.py      
│   ├── crud.py         
│   └── database.py     
├── tests/
│   ├── test_crud.py     
│   └── test_api.py      
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Rodando localmente

```bash
docker-compose up --build
```

A API sobe em `http://localhost:8000` (docs interativas em `/docs`).
> **Observação:** se a porta 3306 já estiver em uso na sua máquina (por um MySQL local instalado fora do Docker), o `docker-compose.yml` expõe o banco na porta 3307 (`3307:3306`) para evitar conflito. A aplicação continua acessando o banco normalmente pela rede interna do Docker. É necessário ter o **Docker Desktop aberto e rodando** antes de executar o comando acima.

## Rodando os testes

```bash
pip install -r requirements.txt
pytest -v
```

## Estratégia de branches (Trunk-Based)

- `main`: branch principal, sempre estável e protegida.
- Desenvolvimento em branches curtas a partir da `main`: `feat/nome-da-funcionalidade`, `fix/nome-do-bug`.
- Toda mudança entra via Pull Request para `main`, nunca commit direto.


## Divisão de funções da equipe

| Integrante | Função |
|---|---|
| _Fernanda Soares Beleza_ | Desenvolvedor(a) |
| _Rafaela Silva_ | Qualidade |
| _Isabella Santiago_ | Operações/Infraestrutura |

## Marco 1: Integração Contínua(CI) e Conteinerização Inicial

Para a atividade de avaliação do dia 09/09/2026, foi feito:
- Repositório Git Estruturado em Trunk Based;
- Código-fonte com Testes Automatizados;
- Pipeline de CI Operacional
