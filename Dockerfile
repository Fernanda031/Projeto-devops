# Estágio 1: instala as dependências
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Estágio 2: imagem final, só com o necessário
FROM python:3.11-slim
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}

WORKDIR /code
COPY --from=builder /install /usr/local
COPY ./app ./app

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]