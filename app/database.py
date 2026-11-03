import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Em produção/dev, usamos MySQL. Nos testes (CI), sobrescrevemos via env var
# para usar SQLite em memória, o que deixa a suíte de testes rápida e sem
# depender de um servidor MySQL rodando localmente.
# Sem credenciais no código: em produção a URL vem da variável de ambiente.
# Sem a variável, usa SQLite local (bom para desenvolvimento e testes).
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
